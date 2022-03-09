<template>
  <div
    align="left"
    style="margin-top: 50px; margin-left: 100px; margin-right: 100px"
  >
    <div>
      <h1 class="section">Explore</h1>
      <!-- <p>The explore feature will be introduced later.</p> -->

      <div>
        Action class:
        <a-select
          ref="select"
          v-model:value="class_id"
          style="min-width: 200px"
          :options="actionOptions"
          @select="getVideoOptions"
        >
        </a-select>
      </div>

      <div v-if="class_id !== null" style="margin-top: 20px">
        Video:
        <a-select
          ref="select"
          v-model:value="video_id"
          style="min-width: 200px"
          :options="videoOptions"
        >
        </a-select>
      </div>
      <a-button
        v-if="video_id !== null"
        type="primary"
        style="margin-top: 20px"
        @click="explore"
        >Search</a-button
      >
      <Skeleton3d
        ref="skeleton3dRef"
        :visible="display"
        :dataPath="exploreData"
        :class_id="class_id"
        :video_id="video_id"
      />
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import Skeleton3d from "../components/Skeleton3d.vue";

export default defineComponent({
  name: "Explore",
  components: { Skeleton3d },
  data() {
    return {
      class_id: null,
      video_id: null,

      actionOptions: [],
      videoOptions: [],
      display: false,
      exploreData: "../database/skeletons_3d/abseiling/abseiling_000.json",
    };
  },
  methods: {
    getVideoOptions(action) {
      this.video_id = null;
      this.videoOptions = [];
      this.display = false;

      let selected_action = this.actionOptions.find((a) => {
        return a.value === action;
      });
      for (let i = 0; i < 1; i++) {
        this.videoOptions.push({
          value: i,
          label: selected_action.label + "_" + String(i).padStart(3, "0"),
        });
      }
    },
    async getActionOptions() {
      await this.axios
        .get("api/v1/action_classes")
        .then((res) => {
          if (res.status === 200) {
            for (let i = 0; i < res.data.data.length; i++) {
              this.actionOptions.push({
                value: res.data.data[i].id,
                label: res.data.data[i].name,
              });
            }
            return;
          }
          throw res;
        })
        .catch((err) => {
          console.log(err);
        });
    },

    explore() {
      this.display = true;
      this.$refs.skeleton3dRef.show();
    },
  },

  mounted() {
    this.getActionOptions();
    this.display = false;
  },
});
</script>

<style scoped>
p {
  font-size: 16px;
}

h1 {
  font-size: 20px;
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
