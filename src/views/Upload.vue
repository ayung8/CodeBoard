<template>
  <v-container>
    <p> Upload or take a photo a clear photo of the whiteboard solution you want to be compiled and run. </p>
    <v-layout row wrap>
      <v-flex xs4>
        <v-img
          :src="require('../assets/photo-illustration.png')"
          class="my-0"
          contain
          height= "500px"
        ></v-img>
      </v-flex>
      <v-spacer></v-spacer>
      <v-flex xs4>
        <v-img
          :src="require('../assets/camera-illustration.png')"
          class="my-0"
          contain
          height= "500px"
        ></v-img>
      </v-flex>
    </v-layout>
    <v-layout>
      <v-flex xs4>
        <v-btn large class="button">
          Upload Picture
        </v-btn>
      </v-flex>
       <v-spacer></v-spacer>
      <v-flex xs4>
         <v-btn large class="button">
            Take Picture
          </v-btn>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
// @ is an alias to /src


export default {
  name: 'Upload',
  components: {

  }
}
</script>