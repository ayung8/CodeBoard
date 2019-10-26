<template>
  <v-container>
    <v-layout
    >
      <v-flex xs12>
        <v-img
          :src="require('../assets/landing-page.png')"
          class="my-0"
          contain
          height= "700px"
        ></v-img>
      </v-flex>
        <router-link :to="'/upload'">
            <v-btn large class="button">
             Start
             </v-btn>
         </router-link>
    </v-layout>
  </v-container>
</template>

<script>
export default {
name: 'landingPage'
}
</script>


<style lang="scss">

.button {
position: absolute;
top: 800px;
right: 200 px;
}
</style>