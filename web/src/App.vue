<template>
  <q-layout view="hHh LpR lFf">
    <!-- 头部 -->
    <q-header bordered class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <q-avatar>
            <img src="./assets/avor.jpeg" />
          </q-avatar>
          Yuyuko
        </q-toolbar-title>
      </q-toolbar>
    </q-header>
    <!-- 菜单 -->
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      :width="200"
      :breakpoint="500"
      bordered
      class="bg-grey-3"
    >
      <q-scroll-area class="fit">
        <q-list>
          <template v-for="(menuItem, index) in menuList" :key="index">
            <q-item
              clickable
              @click="clickItem(menuItem)"
              :active="menuItem.label === activeItem"
              v-ripple
            >
              <q-item-section avatar>
                <q-icon :name="menuItem.icon" />
              </q-item-section>
              <q-item-section>
                {{ menuItem.label }}
              </q-item-section>
            </q-item>
            <q-separator :key="'sep' + index" v-if="menuItem.separator" />
          </template>
        </q-list>
      </q-scroll-area>
    </q-drawer>
    <!-- 内容 -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { ref, defineComponent } from "vue";
import { Item } from "@/lib/types";
import { menuList } from "@/lib/data";

export default defineComponent({
  name: "App",
  setup() {
    return {
      leftDrawerOpen: ref(false),
      activeItem: ref("主页"),
      menuList,
    };
  },
  methods: {
    toggleLeftDrawer() {
      this.leftDrawerOpen = !this.leftDrawerOpen;
    },
    clickItem(item: Item) {
      this.activeItem = item.label;
    },
  },
});
</script>
