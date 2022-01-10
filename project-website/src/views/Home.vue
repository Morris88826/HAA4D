<template>
  <div
    align="left"
    style="margin-top: 50px; margin-left: 100px; margin-right: 100px"
  >
    <div>
      <h1 class="section">Abstract</h1>
      <p>
        Human actions involve complex pose variations, and their 2D projections
        can be highly ambiguous. Thus 3D Spatio-temporal or 4D (i.e., 3D+T)
        human skeletons, which are <b>photometric and viewpoint invariant</b>,
        are an excellent alternative to 2D+T skeletons/pixels to improve action
        recognition accuracy. This paper proposes a <b>new 4D dataset</b>,
        <b>HAA4D</b>, consisting of more than <b>3,300 RGB videos</b> in
        <b>300 human atomic action classes</b>. HAA4D is <b>clean</b>,
        <b>diverse</b>, <b>class-balanced</b> where each class is
        viewpoint-balanced with the use of 4D skeletons, in which as few as one
        4D skeleton per class is sufficient for training a deep recognition
        model. Further, the choice of atomic actions makes annotation even
        easier because each video clip lasts for only a few seconds. All
        training and testing 3D skeletons in HAA4D are <b>globally aligned</b>,
        using a deep alignment model to the same global space, making each
        skeleton face the <b>negative z-direction</b>. Such alignment makes
        matching skeletons more stable by
        <b>reducing intraclass variations</b> and thus with fewer training
        samples per class needed for action recognition. Given the high
        diversity and skeletal alignment in HAA4D, we construct the first
        baseline
        <b>few-shot 4D human atomic action recognition network</b> without bells
        and whistles, which produces comparable or higher performance than
        relevant state-of-the-art techniques relying on embedded space encoding
        without explicit skeletal alignment, using the same small number of
        training samples of unseen classes.
      </p>
      <br />
      <h1>Our Contribution</h1>
      <ol>
        <li>
          HAA4D, a human atomic action dataset where all 4D skeletons are
          globally aligned. HAA4D complements existing prominent 3D+T human
          action datasets such as NTU-RGB+D and Kinetics Skeleton 400. HAA4D
          contains 3390 samples of human actions in the wild with 300 different
          kinds of activities. The samples for each human action range from 2 to
          20, each provided with RGB frames and their corresponding 3D
          skeletons.
        </li>
        <li>
          Introducing an alignment network for predicting orthographic camera
          poses in the train/test samples, where all 4D skeletons are aligned in
          the same camera space, each facing the negative z-direction. This
          allows for better recognition results with a smaller number of
          training samples compared to ST-GCN, Shift-GCN, and SGN.
        </li>
        <li>
          Introduce the first few-shot baseline for 4D human (atomic) action
          recognition that produces results comparable to or better than
          state-of-the-art techniques on unseen classes using a small number of
          training samples.
        </li>
      </ol>
      <br />
      <div>
        <p>
          The 3D skeleton is <b>viewpoint invariant</b>: all train/test 3D
          skeletons in HAA4D are registered by their respective orthographic
          camera pose estimated using our global alignment model. Thus a single
          training 3D skeleton per class is sufficient, in stark contrast to the
          use of 2D RGB images or skeletons, where a large number of training
          data is required, and uneven sampling is an issue.
          <b
            >Trained with as few as one 3D+T or 4D burpee skeleton, the network
            can readily recognize any normalized burpee action shot from any
            viewing angles</b
          >, including those under the person, which are difficult to capture.
          As shown in the figure below, we can use the predicted camera poses to
          rectify views of the input 3D skeletons and bring them to the same
          coordinate system (globally aligned space). This rectification
          provides a <b>stronger correlation between each sample</b> and allows
          us to utilize the explicit information, such as the coordinate of the
          joints, directly for sequence matching and obtain a higher accuracy in
          differentiate the action.
        </p>
        <div style="text-align: center">
          <img
            src="../assets/teaser.png"
            alt="../assets/teaser.png"
            style="width: 80%"
          />
        </div>
      </div>
    </div>
    <br />
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "Home",
  components: {},
  data() {
    return {};
  },
  methods: {},
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
