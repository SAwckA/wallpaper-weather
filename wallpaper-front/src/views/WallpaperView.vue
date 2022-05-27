<template>
    <div class="root">

        <WallpaperComponent />
    </div>
</template>

<script>

import WallpapperComponent from '../components/WallpaperComponent'
import WallpaperComponent from '../components/WallpaperComponent.vue'

export default {
    name: "wallpaper-view",
    component: WallpapperComponent,
    components: { WallpaperComponent }
}
</script>
