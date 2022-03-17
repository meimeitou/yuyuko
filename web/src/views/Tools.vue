<template>
  <div class="q-pa-md q-gutter-sm">
    <q-btn color="white" text-color="black" label="Standard" />
    <q-btn color="secondary" label="Secondary" />
    <q-btn color="amber" glossy label="Amber" @click="alert" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import tools from "@/lib/tools";
export default defineComponent({
  name: "tools",
  methods: {
    alert() {
      tools.errMsg("sdf");
    },
  },
});
</script>
