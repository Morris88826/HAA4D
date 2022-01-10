<template>
  <div id="myDiv"></div>
  <a-slider
    v-if="showSlider"
    v-model:value="frame_id"
    :tooltip-visible="true"
    :min="frames.min"
    :max="frames.max"
    @change="changeFrame"
  />
</template>

<script>
import { defineComponent, watch } from "vue";
import Plotly from "plotly.js-dist-min";

export default defineComponent({
  name: "Skeleton3d",
  props: ["visible", "dataPath", "class_id", "video_id"],
  components: {},
  data() {
    return {
      showSlider: false,
      frame_id: 0,
      frames: {
        min: 0,
        max: 0,
      },

      data: [],

      bones: [
        [0, 1],
        [1, 2],
        [2, 3],
        [0, 4],
        [4, 5],
        [5, 6],
        [0, 7],
        [7, 8],
        [8, 9],
        [9, 10],
        [8, 11],
        [11, 12],
        [12, 13],
        [8, 14],
        [14, 15],
        [15, 16],
      ],

      joint_name: [
        "lower_spine",
        "right_hip",
        "right_knee",
        "right_ankle",
        "left_hip",
        "left_knee",
        "left_ankle",
        "mid_spine",
        "upper_spine",
        "neck",
        "nose",
        "left_shoulder",
        "left_elbow",
        "left_hand",
        "right_shoulder",
        "right_elbow",
        "right_hand",
      ],
    };
  },
  methods: {
    createPlot(frame = 0) {
      var bones = [];
      let data = this.data[frame].data;

      for (let i = 0; i < this.bones.length; i++) {
        let s = this.bones[i][0];
        let e = this.bones[i][1];
        let s_joint = data[s];
        let e_joint = data[e];

        var bone = {
          type: "scatter3d",
          x: [s_joint[0], e_joint[0]],
          y: [s_joint[1], e_joint[1]],
          z: [s_joint[2], e_joint[2]],
          mode: "lines+markers+text",
          name: "(" + this.joint_name[s] + ") - (" + this.joint_name[e] + ")",
          text: [this.joint_name[s], this.joint_name[e]],
          textposition: "top",
          width: 5,
          marker: { size: 5 },
        };

        bones.push(bone);
      }

      var layout = {
        autosize: false,
        width: 1000,
        height: 500,
        font: {
          size: 8,
        },
        scene: {
          aspectmode: "manual",
          aspectratio: {
            x: 1,
            y: 1,
            z: 1,
          },
          xaxis: { range: [-1, 1] },
          yaxis: { range: [-1, 1] },
          zaxis: { range: [-1, 1] },
          camera: {
            up: { x: 0, y: -1, z: 0 },
            eye: {
              x: 0,
              y: 0,
              z: -2,
            },
          },
        },
      };

      Plotly.newPlot(document.getElementById("myDiv"), bones, layout);
    },

    _handleData(dataString) {
      const dS = dataString.split(",");

      let d = [];
      for (let i = 0; i < dS.length; i++) {
        d.push(parseFloat(dS[i]));
      }
      return d;
    },
    handleData(data) {
      let d = {
        class_id: data.class_id,
        video_id: data.video_id,
        frame_id: data.frame_id,
        data: [
          this._handleData(data.lower_spine),
          this._handleData(data.right_hip),
          this._handleData(data.right_knee),
          this._handleData(data.right_ankle),
          this._handleData(data.left_hip),
          this._handleData(data.left_knee),
          this._handleData(data.left_ankle),
          this._handleData(data.mid_spine),
          this._handleData(data.upper_spine),
          this._handleData(data.neck),
          this._handleData(data.nose),
          this._handleData(data.left_shoulder),
          this._handleData(data.left_elbow),
          this._handleData(data.left_hand),
          this._handleData(data.right_shoulder),
          this._handleData(data.right_elbow),
          this._handleData(data.right_hand),
        ],
      };

      return d;
    },

    async getSkeletons(class_id, video_id) {
      return this.axios.post("api/v1/skeletons_3d", {
        class_id: class_id,
        video_id: video_id,
      });
    },

    changeFrame() {
      this.createPlot(this.frame_id);
    },

    show() {
      this.frame_id = 0;
      this.getSkeletons(this.class_id, this.video_id)
        .then((res) => {
          if (res.status === 200) {
            this.data = [];
            for (let i = 0; i < res.data.data.length; i++) {
              this.data.push(this.handleData(res.data.data[i]));
            }

            if (this.data.length > 0) {
              document.getElementById("myDiv").style.display = "block";
              this.createPlot();
              this.frames = {
                min: 0,
                max: this.data.length,
              };
              this.showSlider = true;
            }
            return;
          }
          throw res;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },

  mounted() {
    watch(
      () => this.visible,
      () => {
        if (this.visible == false) {
          document.getElementById("myDiv").style.display = "none";
          this.showSlider = false;
        }
      }
    );
  },
});
</script>

<style scoped></style>
