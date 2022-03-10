<template>
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
          <q-item clickable v-ripple exact :to="menuItem.to">
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
</template>

<script lang="ts">
import { ref, defineComponent } from "vue";
import { menuList } from "@/lib/data";

export default defineComponent({
  data() {
    return {
      leftDrawerOpen: this.open,
      activeItem: ref("Home"),
      menuList,
    };
  },
  props: {
    open: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    toggleLeftDrawer() {
      this.leftDrawerOpen = !this.leftDrawerOpen;
    },
  },
});
</script>
