<template>
  <a-layout class="layout">
    <a-layout-header style="height: 200px">
      <div>
        <div class="row-12">
          <h1 style="text-align: center; margin: auto; font-size: 60px">
            {{ projectTitle }}
          </h1>
        </div>
        <div class="row-12">
          <h3 style="text-align: center; margin: auto">
            {{ projectSubTitle }}
          </h3>
        </div>
      </div>
    </a-layout-header>
    <a-layout-content style="background: #fff">
      <a-menu theme="dark" mode="horizontal" :style="{ lineHeight: '64px' }">
        <router-link :to="{ name: 'home' }">
          <a-menu-item key="home">Home</a-menu-item>
        </router-link>

        <router-link :to="{ name: 'dataset' }">
          <a-menu-item key="dataset">Dataset</a-menu-item>
        </router-link>

        <router-link :to="{ name: 'annotationTool' }">
          <a-menu-item key="tool">Annotation Tool</a-menu-item>
        </router-link>

        <router-link :to="{ name: 'explore' }">
          <a-menu-item key="explore">Explore</a-menu-item>
        </router-link>

        <router-link :to="{ name: 'others' }">
          <a-menu-item key="others">Others</a-menu-item>
        </router-link>
      </a-menu>
      <slot />
    </a-layout-content>
  </a-layout>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "Layout",
  components: {},
  data() {
    return {
      projectTitle: "HAA4D",
      projectSubTitle:
        "Few-Shot Human Atomic Action Recognition via 3D Spatio-Temporal Skeletal Alignment",
    };
  },
  methods: {},
});
</script>

<style scoped>


.ant-layout-header {
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ant-menu-item-selected {
  background-color: #001529 !important;
  color: rgba(255, 255, 255, 0.65) !important;
}
</style>
