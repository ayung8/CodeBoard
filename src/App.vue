<template>
  <v-app>
    <!-- <v-app-bar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Code</span>
        <span class="font-weight-light">Board</span>
      </v-toolbar-title>
      <v-spacer></v-spacer> -->
      <v-btn
        text
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
      >
      </v-btn>
    <!-- </v-app-bar> -->

      <router-view />

  </v-app>
</template>

<script>


export default {
  name: 'App',
  components: {
  },
  data: () => ({
    //
  }),
};
</script>
