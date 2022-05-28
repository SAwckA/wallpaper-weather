<template>
    <div class="wallpaper-root">
        <span class="description location">{{ location.name }} {{ location.region }} {{ location.country }} </span>
        <span class="description"> ->  
            <span v-if="isDay === 1" class="description">День</span>
            <span v-if="isDay === 0" class="description">Ночь</span>
            | {{ weatherText }} | температура: {{ temperature.temp }}°C | по ощущениям: {{ temperature.feelslike }}°C</span>
        <!-- <img v-if="isCloudy" src="@/assets/rain.jpg"> -->
        <!-- <img v-show="(weatherCode - 200) >= 0 & (weatherCode - 200) < 100" src="@/assets/200.jpg" class="wallpaper">
        <img v-show="(weatherCode - 300) >= 0 & (weatherCode - 300) < 100" src="@/assets/300.jpg" class="wallpaper">
        <img v-show="(weatherCode - 600) >= 0 & (weatherCode - 600) < 100" src="@/assets/600.jpg" class="wallpaper">
        <img v-show="(weatherCode - 500) >= 0 & (weatherCode - 500) < 100" src="@/assets/rain.jpg" class="wallpaper">
        <img v-show="(weatherCode - 700) >= 0 & (weatherCode - 700) < 100" src="@/assets/700.jpg" class="wallpaper">
        <img v-show="(weatherCode - 800) >= 0 & (weatherCode - 800) < 100" src="@/assets/800.jpg" class="wallpaper">
        <img v-show="weatherCode === 900" src="@/assets/800.jpg" class="wallpaper"> -->
        <img v-show="weatherCode === 1000 & isDay===1 " src="@/assets/sunny_d.jpg" class="wallpaper">
        <img v-show="weatherCode === 1000 & isDay===0 " src="@/assets/sunny_n.jpg" class="wallpaper">
        
        <img v-show="([1003, 1006].includes(weatherCode)) & isDay===1 " src="@/assets/cloudy_d.jpg" class="wallpaper">
        <img v-show="([1003, 1006].includes(weatherCode)) & isDay===0 " src="@/assets/cloudy_n.jpg" class="wallpaper">

        <img v-show="([1009].includes(weatherCode)) & isDay===1 " src="@/assets/overcast_d.jpg" class="wallpaper">
        <img v-show="([1009].includes(weatherCode)) & isDay===0 " src="@/assets/overcast_n.jpg" class="wallpaper">

        <!-- Туман -->
        <img v-show="([1030, 1135, 1147].includes(weatherCode)) & isDay===1 " src="@/assets/fog_d.jpg" class="wallpaper">
        <img v-show="([1030, 1135, 1147].includes(weatherCode)) & isDay===0 " src="@/assets/fog_n.jpg" class="wallpaper">

        <img v-show="([1063, 1072].includes(weatherCode)) & isDay===1 " src="@/assets/patchy_rain_nearby_d.jpg" class="wallpaper">
        <img v-show="([1063, 1072].includes(weatherCode)) & isDay===0 " src="@/assets/patchy_rain_nearby_n.jpg" class="wallpaper">

        <img v-show="([1066, 1069].includes(weatherCode)) & isDay===1 " src="@/assets/patchy_snow_nearby_d.jpg" class="wallpaper">
        <img v-show="([1066, 1069].includes(weatherCode)) & isDay===0 " src="@/assets/patchy_snow_nearby_n.jpg" class="wallpaper">

        <!-- Грозы -->
        <img v-show="([1087,
                                      1273, 1276, 1279, 1282].includes(weatherCode)) & isDay===1 " src="@/assets//thundery_outbreaks_in_nearby_d.jpg" class="wallpaper">

        <img v-show="([1087,
                                      1273, 1276, 1279, 1282].includes(weatherCode)) & isDay===0 " src="@/assets//thundery_outbreaks_in_nearby_n.jpg" class="wallpaper">

        <img v-show="([1114, 1117].includes(weatherCode))  & isDay===1 " src="@/assets/blowing_snow_d.jpg" class="wallpaper">
        <img v-show="([1114, 1117].includes(weatherCode))  & isDay===0 " src="@/assets/blowing_snow_n.jpg" class="wallpaper">

        <img v-show="([1150, 1153].includes(weatherCode)) & isDay===1 " src="@/assets/light_drizzle_d.jpg" class="wallpaper">
        <img v-show="([1150, 1153].includes(weatherCode)) & isDay===1 " src="@/assets/light_drizzle_n.jpg" class="wallpaper">


        <!-- Дождь  -->
        <img v-show="([1168, 1171, 1180, 1183, 1186, 1189, 1192, 1195, 1198, 1201, 1240, 1243, 1246, 1249, 1252, 1255, 1258, 1261, 1264].includes(weatherCode)) & isDay===1 " src="@/assets/heavy_rain_d.jpg" class="wallpaper">

        <img v-show="([1168, 1171, 1180, 1183, 1186, 1189, 1192, 1195, 1198, 1201, 1240, 1243, 1246, 1249, 1252, 1255, 1258, 1261, 1264].includes(weatherCode)) & isDay===0 " src="@/assets/heavy_rain_n.jpg" class="wallpaper">


        <!-- Снег -->
        <img v-show="([1204, 1207, 1210, 1213, 1216, 1219, 1222, 1225, 1237].includes(weatherCode)) & isDay===1 " src="@/assets/blowing_snow_d.jpg" class="wallpaper">
        <img v-show="([1204, 1207, 1210, 1213, 1216, 1219, 1222, 1225, 1237].includes(weatherCode)) & isDay===0 " src="@/assets/blowing_snow_n.jpg" class="wallpaper">
    </div>
</template>

<script>
export default {
    data () {
        return {
                altitude: 43.026257,
                longitude: 131.887430,
                weatherCode: null,
                weatherText: null,
                isDay: null,
                temperature: {
                    temp: null,
                    feelslike: null
                },
                connection: null,
                location: {
                    name: null,
                    region: null,
                    country: null
                }
            }
    },
    created() {
        console.log(this.$route.query)
        if (this.$route.query.altitude) {
            this.altitude = this.$route.query.altitude
        }
        if (this.$route.query.longitude) {
            this.longitude = this.$route.query.longitude
        }
        this.connection = new WebSocket(`ws://localhost:8000/ws?altitude=${this.altitude}&longitude=${this.longitude}`);
        this.connection.onmessage = (event) => {
            let data = JSON.parse(event.data);
            this.sendMessage("OK");
            console.log(data)
            this.weatherCode = data.current.condition.code
            this.weatherText = data.current.condition.text
            this.isDay = data.current.is_day
            this.location.name = data.location.name
            this.location.region = data.location.region
            this.location.country = data.location.country
            this.temperature.temp = data.current.temp_c
            this.temperature.feelslike = data.current.feelslike_c
            console.log(this.weatherCode)
            console.log(this.isDay)
        }
        this.connection.onopen = () => {
            this.sendMessage('OPEN')
        }
        this.connection.onclose = () => {
            this.sendMessage('CLOSE')
        }
    },
    methods: {
        sendMessage: function(message) {
            this.connection.send(message);
        }
    },
    unmounted() {
        this.sendMessage('CLOSE')
        this.connection.close()
    }

}
</script>

<style scoped>
    .wallpaper {
        position: absolute;
        top: 0;
        left: 0;
        max-width: 100vw;
        max-height: 100vh;
        object-fit: cover;
        min-width: 100vh;
        min-height: 100vh;
        width: 1920px;
        height: 1080px;
    }
    
    .description{
        z-index: 10;
        position: relative;
        color: white;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 2vh;
        text-shadow: 1px 0 1px #000, 
                    0 1px 1px #000, 
                    -1px 0 1px #000, 
                    0 -1px 1px #000;
    }

    .location{
        font-size: 3vh;
    }

    .wallpaper-root{
        position: relative;
    }

    body, html{
        padding: 0;
        margin: 0;
    }
</style>