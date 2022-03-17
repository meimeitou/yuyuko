<template>
  <q-layout view="hHh LpR lFf">
    <!-- 头部 -->
    <q-header bordered class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggle" />
        <q-toolbar-title>
          <q-avatar>
            <img src="./assets/avor.jpeg" />
          </q-avatar>
          Yuyuko
        </q-toolbar-title>
      </q-toolbar>
    </q-header>
    <Drawer ref="drawerRef" :open="leftDrawerOpen"></Drawer>
    <!-- 内容 -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
  <div id="masterfooter">
    Copyright © 2022 - 2022
    <a
      class="doc-link q-ml-xs"
      href="https://github.com/roygbip/yuyuko"
      target="_blank"
      rel="noopener"
      >@TonyYin<span class="q-icon" aria-hidden="true" role="presentation"
        ><svg viewBox="0 0 24 24">
          <path
            d="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z"
          ></path></svg></span
    ></a>
  </div>
</template>

<script lang="ts">
import { ref, defineComponent } from "vue";
import Drawer from "@/components/Drawer.vue";

export default defineComponent({
  name: "App",
  setup() {
    const drawerRef = ref<InstanceType<typeof Drawer>>();
    const toggle = () => {
      drawerRef.value?.toggleLeftDrawer();
    };

    return {
      toggle,
      drawerRef,
      leftDrawerOpen: ref(false),
    };
  },
  components: {
    Drawer,
  },
  methods: {},
});
</script>

<style type="text/css" scoped>
#masterfooter {
  position: absolute;
  left: 50%;
  bottom: 0;
  text-align: center;
}
</style>
