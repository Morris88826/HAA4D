<template>
  <div
    align="left"
    style="margin-top: 50px; margin-left: 100px; margin-right: 100px"
  >
    <div>
      <h1 class="section">HAA4D Dataset</h1>
      <p>
        HAA4D is a challenging human action recognition 3D+T dataset that is
        built on top of the HAA500 dataset. HAA500 is a curated video dataset
        consisting of atomic hu-man action video clips, which provides
        diversified poseswith variation and examples closer to real-life
        activities. Similar to Kinetics, the original dataset provides solely
        in-the-wild RGB videos. However, instead of using existing 2D joints
        prediction networks, which often produce inaccurate results when joints
        are hidden or not present, HAA4D consists of hand-labeled 2D human
        skeletons position. These accurate features can not only increase
        theprecision of the 3D ground-truth skeleton but also benefit training
        for new joints prediction models that can reasonably hallucinate
        out-of-frame joints. The labeled 2D joints will then be raised to 3D
        using EvoSkeleton. HAA4Dis thus named with its accurate per-frame 3D
        spatial andtemporal skeletons for human atomic actions.
      </p>
      <h1>1. Action Classes</h1>
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
      <br />
      <h1>2. Dataset Details</h1>
      <h3>2.1 Comparison with other pubic datasets</h3>
      <a-table
        :data-source="datasetComparison"
        :columns="datasetComparisonCol"
        :pagination="false"
      />
      <br />
      <h3>2.2 Dataset Summary</h3>
      <a-table
        :data-source="datasetSummary.data"
        :columns="datasetSummary.cols"
        :pagination="false"
      />

      <br />
      <h3>2.3 Evaluation Benchmark</h3>
      <p>
        For actions with 20 examples per class, video indexes 0 to 9 are used
        for training, while videos from 10 to 19 are used for testing. We
        perform data augmentation on the first ten samples, and among all,
        videos 8 and 9 are used for validation. For actions that contain only
        two samples, the one with a smaller index serves as the query, and the
        other serves as the support.
      </p>
      <br />
      <br />
      <h1>3. Examples</h1>
      <p>
        Here we provide some examples in our HAA4D dataset. The image on the
        left shows the 8-frame sampling from different actions. We use our
        global alignment model (GAM) to rectify the input skeletons and bring
        them to the same coordinate system that all actions start at facing the
        negative z-direction. Some samples of globally aligned skeletons can be
        seen on the right. More samples can be access in
        <router-link :to="{ name: 'explore' }">
          <a>here</a>
        </router-link>
        .
      </p>

      <div>
        <img
          src="../assets/8-frames.png"
          alt="../assets/8-frames.png"
          style="width: 50%"
        />
        <img
          src="../assets/example.png"
          alt="../assets/example.png"
          style="width: 50%"
        />
      </div>
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

      datasetComparisonCol: [
        {
          title: "Dataset",
          dataIndex: "dataset",
          key: "dataset",
        },
        {
          title: "Samples",
          dataIndex: "samples",
          key: "samples",
        },
        {
          title: "Actions",
          dataIndex: "actions",
          key: "actions",
        },
        {
          title: "Views",
          dataIndex: "views",
          key: "views",
        },
        {
          title: "Modalities",
          dataIndex: "modalities",
          key: "modalities",
        },
        {
          title: "Year",
          dataIndex: "year",
          key: "year",
        },
      ],

      datasetComparison: [
        {
          key: 1,
          dataset: "UWA3D Multiview II",
          samples: 1075,
          actions: 30,
          views: 5,
          modalities: "RGB+D+3DJoints",
          year: 2015,
        },
        {
          key: 2,
          dataset: " NTU RGB+D",
          samples: 56880,
          actions: 60,
          views: 80,
          modalities: "RGB+D+IR+3DJoints",
          year: 2016,
        },
        {
          key: 3,
          dataset: "SYSU 3DHOI",
          samples: 480,
          actions: 12,
          views: 1,
          modalities: "RGB+D+3DJoints",
          year: 2017,
        },
        {
          key: 4,
          dataset: "Kinetics 400",
          samples: 306245,
          actions: 400,
          views: null,
          modalities: "RGB",
          year: 2017,
        },
        {
          key: 5,
          dataset: "NTU RGB+D 120",
          samples: 114480,
          actions: 120,
          views: 155,
          modalities: "RGB+D+IR+3DJoints",
          year: 2019,
        },
        {
          key: 6,
          dataset: "Kinetics-700-2020",
          samples: 633728,
          actions: 700,
          views: null,
          modalities: "RGB",
          year: 2020,
        },
        {
          key: 7,
          dataset: "Ego4D",
          samples: 3025,
          actions: 110,
          views: null,
          modalities: "RGB+3DMeshes+Audio",
          year: 2021,
        },
        {
          key: 8,
          dataset: "HAA4D",
          samples: 3390,
          actions: 300,
          views: "2/20",
          modalities: "RGB+3DJoints",
          year: 2021,
        },
      ],

      datasetSummary: {
        cols: [
          {
            title: "Classes",
            dataIndex: "classes",
            key: "classes",
          },
          {
            title: "Total Samples",
            dataIndex: "total_samples",
            key: "total_samples",
          },
          {
            title: "Globally Aligned Samples",
            dataIndex: "globally_aligned_samples",
            key: "globally_aligned_samples",
          },
          {
            title: "Total Frames",
            dataIndex: "total_frames",
            key: "total_frames",
          },
          {
            title: "Min Frames",
            dataIndex: "min_frames",
            key: "min_frames",
          },
          {
            title: "Max Frames",
            dataIndex: "max_frames",
            key: "max_frames",
          },
          {
            title: "Average Frames",
            dataIndex: "average_frames",
            key: "average_frames",
          },
          {
            title: "2 Examples",
            dataIndex: "examples_2",
            key: "examples_2",
          },
          {
            title: "20 Examples",
            dataIndex: "examples_20",
            key: "examples_20",
          },
          {
            title: "Person per Example",
            dataIndex: "person_per_example",
            key: "person_per_example",
          },
        ],
        data: [
          {
            key: 1,
            classes: 300,
            total_samples: 3390,
            globally_aligned_samples: 400,
            total_frames: 212042,
            min_frames: 7,
            max_frames: 757,
            average_frames: 63,
            examples_2: "145 classes",
            examples_20: "155 classes",
            person_per_example: 1,
          },
        ],
      },
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

h1 {
  font-size: 20px;
}

h3 {
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
