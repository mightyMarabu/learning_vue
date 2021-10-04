<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld :msg="message"/>
    <input type="text" v-model="message" />
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
export default {
  name: 'app',
  components: {
    HelloWorld
  },
  data(){
    return {
      message: 'Hello World!'
    }
  }
}
</script>

// styles omitted