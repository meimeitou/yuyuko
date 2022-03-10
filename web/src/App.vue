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
