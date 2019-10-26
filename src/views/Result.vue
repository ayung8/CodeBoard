<template>
  <v-container>
    <v-layout>
      <v-flex xs12>
        <v-img
          :src="require('../assets/summary-illustration.png')"
          class="my-0"
          contain
          height= "330px"
        ></v-img>
      </v-flex>
      </v-layout>
      <v-layout>
        <v-flex xs12>
            <p>
                Code compiled successfully
                <br>
                Run time:
                <br>
                Outputs:
            </p>
            </v-flex >
        </v-layout>
        <router-link :to="'/'">
            <v-btn large class="button">
             Restart
             </v-btn>
         </router-link>
  </v-container>
</template>

<script>
// @ is an alias to /src


export default {
  name: 'Result',
  components: {

  }
}
</script>