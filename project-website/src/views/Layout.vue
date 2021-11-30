<template>
  <a-layout class="layout">
    <a-layout-header style="height: 150px">
      <div class="row-12" style="font-size: xxx-large">
        <h1 style="text-align: center; margin-top: 25px; margin-bottom: 0px">
          {{ projectTitle }}
        </h1>
      </div>
      <div class="row-12">
        <h1 style="text-align: center">{{ projectSubTitle }}</h1>
      </div>
    </a-layout-header>
    <a-layout-content style="background: #fff">
      <a-menu
        theme="dark"
        mode="horizontal"
        v-model:selectedKeys="selectedKeys"
        :style="{ lineHeight: '64px' }"
      >
        <a-menu-item key="home">Home</a-menu-item>
        <a-menu-item key="tool">Annotation Tool</a-menu-item>
        <a-menu-item key="explore">Explore</a-menu-item>
        <a-menu-item key="downloads">Downloads</a-menu-item>
      </a-menu>
      <Home v-if="selectedKeys[0] === 'home'" />
      <!-- <div align="left" style="margin-top: 50px; margin-left: 100px; margin-right: 100px;" v-if="selectedKeys[0] === 'home'">
        <div>
          <h1 class="section">Overview</h1>
          <p>
            This page introduces a new 4D dataset, <b>HAA4D</b>, consisting of
            more than <b>3,300</b> RGB videos in <b>300</b> single-person atomic
            action classes.
          </p>
          <p>
            HAA4D is <b>clean</b>, <b>diverse</b>, <b>class-balanced</b> where
            each class is viewpoint-balanced with the use of 3D+T or 4D
            skeletons.
          </p>
          <p>
            The dataset contains <b>RGB images</b>, <b>2D</b>, and
            <b>3D</b> skeletons. Parts of the dataset contain additional
            globally aligned skeleton where action sequences are rotated to face
            in the <b>negative z</b> direction.
          </p>

          <p>
            Currently, there are 300 classes of human actions. <b>155</b> of
            them contain <b>20 samples per class</b>, while the rest classes
            have <b>2 samples per class</b>.
          </p>

          <p>
            Unlike Kinetics-Skeleton, HAA4D consists of hand-labeled 2D human
            skeletons position where the accuracy will not be subject to
            occluded or out-of-bound joints. Thus, it increases the precision of
            the 3D ground-truth skeleton and benefits training for new joint
            prediction models that can reasonably hallucinate out-of-frame
            joints. The labeled 2D joints will then be raised to 3D using
            EvoSkeleton.
          </p>

          <p>
            We also provide an annotation tool that can help users with faster
            labeling. We hope that by providing this annotation tool, the
            dataset can become more comprehensive in the future to cover more
            human action poses, contributing to research in few-shot human pose
            estimation and action recognition that utilizes 3D+T data.
          </p>
        </div>
        <br />
        <div>
          <h1 class="section">1. Action Classes</h1>
          <h3>20 examples per class</h3>
          <table>
            <tr v-for="(row, i) in createTable(jsonData.class_20)" :key="i">
              <td v-for="(action, j) in row" :key="action">
                <p style="font-size: 12px; margin: auto">
                  {{ getIdex(i, j, 1) }}: {{ action }}
                </p>
              </td>
            </tr>
          </table>
          <br />
          <h3>2 examples per class</h3>
          <table>
            <tr v-for="(row, i) in createTable(jsonData.class_2)" :key="i">
              <td v-for="(action, j) in row" :key="action">
                <p style="font-size: 12px; margin: auto">
                  {{ getIdex(i, j, 156) }}: {{ action }}
                </p>
              </td>
            </tr>
          </table>
          <br />
          <h1>2. Globally Aligned Skeletons</h1>
          <table>
            <tr v-for="(row, i) in createTable(jsonData.class_global)" :key="i">
              <td v-for="(action, j) in row" :key="action">
                <p style="font-size: 12px; margin: auto">
                  {{ getIdex(i, j, 1) }}: {{ action }}
                </p>
              </td>
            </tr>
          </table>
          <br />
        </div>
      </div> -->
    </a-layout-content>
  </a-layout>
</template>

<script>
import { defineComponent } from "vue";
import Home from "./Home.vue";

export default defineComponent({
  name: "Layout",
  components: { Home },
  data() {
    return {
      projectTitle: "HAA4D",
      projectSubTitle:
        "Few-Shot Human Atomic Action Recognition via 3D Spatio-Temporal Skeletal Alignment",
      selectedKeys: ["home"],
    };
  },
  methods: {},
});
</script>

<style scoped>
.ant-layout-header {
  background: #fff;
}

.ant-menu-item-selected {
  background-color: #001529 !important;
  color: rgba(255, 255, 255, 0.65) !important;
}
</style>
