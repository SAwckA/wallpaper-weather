<template>
    <div class="wallpaper-root">
        <span class="description">{{ weatherCode }}</span>
        <!-- <img v-if="isCloudy" src="@/assets/rain.jpg"> -->
        <img v-show="(weatherCode - 200) >= 0 & (weatherCode - 200) < 100" src="@/assets/200.jpg" class="wallpaper">
        <img v-show="(weatherCode - 300) >= 0 & (weatherCode - 300) < 100" src="@/assets/300.jpg" class="wallpaper">
        <img v-show="(weatherCode - 600) >= 0 & (weatherCode - 600) < 100" src="@/assets/600.jpg" class="wallpaper">
        <img v-show="(weatherCode - 500) >= 0 & (weatherCode - 500) < 100" src="@/assets/rain.jpg" class="wallpaper">
        <img v-show="(weatherCode - 700) >= 0 & (weatherCode - 700) < 100" src="@/assets/700.jpg" class="wallpaper">
        <img v-show="(weatherCode - 800) >= 0 & (weatherCode - 800) < 100" src="@/assets/800.jpg" class="wallpaper">
        <img v-show="weatherCode === 900" src="@/assets/800.jpg" class="wallpaper">
    </div>
</template>

<script>
export default {
    data () {
        return {
                altitude: 43.026257,
                longitude: 131.887430,
                weatherCode: null,
                connection: null
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
        this.connection = new WebSocket(`ws://0.0.0.0:8000/ws?altitude=${this.altitude}&longitude=${this.longitude}`);
        this.connection.onmessage = (event) => {
            let data = JSON.parse(event.data).data;
            this.sendMessage("OK");
            this.weatherCode = data[0].weather.code
            console.log(this.weatherCode)
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
        /* max-height: 100vh; */
        object-fit: fill;
    }
    
    .description{
        z-index: 10;
        position: relative;
        color: white;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 4vh;
    }

    .wallpaper-root{
        position: relative;
    }

    body, html{
        padding: 0;
        margin: 0;
    }
</style>