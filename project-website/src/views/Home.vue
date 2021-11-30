<template>
  <div
    align="left"
    style="margin-top: 50px; margin-left: 100px; margin-right: 100px"
  >
    <div>
      <h1 class="section">Overview</h1>
      <p>
        This page introduces a new 4D dataset, <b>HAA4D</b>, consisting of more
        than <b>3,300</b> RGB videos in <b>300</b> single-person atomic action
        classes.
      </p>
      <p>
        HAA4D is <b>clean</b>, <b>diverse</b>, <b>class-balanced</b> where each
        class is viewpoint-balanced with the use of 3D+T or 4D skeletons.
      </p>
      <p>
        The dataset contains <b>RGB images</b>, <b>2D</b>, and
        <b>3D</b> skeletons. Parts of the dataset contain additional globally
        aligned skeleton where action sequences are rotated to face in the
        <b>negative z</b> direction.
      </p>

      <p>
        Currently, there are 300 classes of human actions. <b>155</b> of them
        contain <b>20 samples per class</b>, while the rest classes have
        <b>2 samples per class</b>.
      </p>

      <p>
        Unlike Kinetics-Skeleton, HAA4D consists of hand-labeled 2D human
        skeletons position where the accuracy will not be subject to occluded or
        out-of-bound joints. Thus, it increases the precision of the 3D
        ground-truth skeleton and benefits training for new joint prediction
        models that can reasonably hallucinate out-of-frame joints. The labeled
        2D joints will then be raised to 3D using EvoSkeleton.
      </p>

      <p>
        We also provide an annotation tool that can help users with faster
        labeling. We hope that by providing this annotation tool, the dataset
        can become more comprehensive in the future to cover more human action
        poses, contributing to research in few-shot human pose estimation and
        action recognition that utilizes 3D+T data.
      </p>
    </div>
    <br />
    <div>
      <h1 class="section">1. Action Classes</h1>
      <h3>1.1 Twenty examples per class ({{ jsonData.class_20.length }})</h3>
      <table>
        <tr v-for="(row, i) in createTable(jsonData.class_20)" :key="i">
          <td v-for="action in row" :key="action">
            <p style="font-size: 12px; margin: auto">
              {{ getIdex(action) }}: {{ action }}
            </p>
          </td>
        </tr>
      </table>
      <br />
      <h3>1.2 Two examples per class ({{ jsonData.class_2.length }})</h3>
      <table>
        <tr v-for="(row, i) in createTable(jsonData.class_2)" :key="i">
          <td v-for="action in row" :key="action">
            <p style="font-size: 12px; margin: auto">
              {{ getIdex(action) }}: {{ action }}
            </p>
          </td>
        </tr>
      </table>
      <br />
      <h3>
        1.3 Globally Aligned Skeletons ({{ jsonData.class_global.length }})
      </h3>
      <table>
        <tr v-for="(row, i) in createTable(jsonData.class_global)" :key="i">
          <td v-for="action in row" :key="action">
            <p style="font-size: 12px; margin: auto">
              {{ getIdex(action) }}: {{ action }}
            </p>
          </td>
        </tr>
      </table>
      <br />
      <h1>2. Dataset Details</h1>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "Home",
  components: {},
  data() {
    return {
      jsonData: null,
      allClasses: [],
      num_cols: 5,
    };
  },
  methods: {
    createTable(items) {
      let table = [];
      let row = [];
      for (let i = 0; i < items.length; i++) {
        row.push(items[i]);
        if ((i + 1) % this.num_cols === 0) {
          table.push(row);
          row = [];
        } else if (i == items.length - 1) {
          table.push(row);
          row = [];
        }
      }
      return table;
    },

    getIdex(action) {
      for (let i = 0; i < this.allClasses.length; i++) {
        if (this.allClasses[i] === action) {
          return i + 1;
        }
      }
      return -1;
    },
  },

  beforeMount() {
    this.jsonData = require("../assets/all_classes.json");
    this.allClasses = [];
    for (let i = 0; i < this.jsonData.class_20.length; i++) {
      this.allClasses.push(this.jsonData.class_20[i]);
    }
    for (let i = 0; i < this.jsonData.class_2.length; i++) {
      this.allClasses.push(this.jsonData.class_2[i]);
    }
  },
});
</script>

<style scoped>
p {
  font-size: 16px;
}

.section {
  font-size: 25px;
}

table {
  width: 100%;
}

td {
  border-style: solid;
  border-width: 1px;
  width: 20%;
}
</style>
