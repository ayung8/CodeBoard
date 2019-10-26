<template>
<v-container>
    <v-layout justify-center row wrap>
        <v-flex xs-12 mt-5>
            <p>Does the code look right? Make any necessary edits</p>
        </v-flex>
    </v-layout>
    <v-layout>
        <v-flex  pa-3>
            <v-text-field
            outlined
            solo
            height="500px"
            width="400px"
            color="#313030"
        ></v-text-field>
        </v-flex>
    </v-layout>
    <v-layout>
        <v-flex xs-12 pa-2>
            <v-text-field
            solo
            height="98px"
            label = "Inputs"
            color="#313030"
        ></v-text-field>
        </v-flex>
    </v-layout>
    <v-layout>
        <v-flex>
            <v-btn large class="button">
                Submit
            </v-btn>
        </v-flex>
    </v-layout>
   </v-container>
</template>

<script>
export default {
  name: "Input",
  data: () => ({
   code: "[abc]"
  }),
  methods: {
    // onChange(value) {
    //   this.$emit("change", value);
    // }
  }
}
</script>

<style>

</style>