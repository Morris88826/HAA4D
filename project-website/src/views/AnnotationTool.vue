<template>
  <div
    align="left"
    style="margin-top: 50px; margin-left: 100px; margin-right: 100px"
  >
    <div>
      <h1 class="section">Annotation Tool</h1>
      <p>
        To help expand the dataset to more actions and classes, we have
        developed a simple interactive annotation tool that supports faster user
        labeling. The annotation tool provides the end-to-end creation of
        accurate 3D skeletons from 2D images. This page will show the main
        functionalities of the annotation tool and how to set it up so that we
        can easily create more distinct action classes through crowdsourcing.
      </p>
      <br />
      <h1>Get Started</h1>

      <div class="container">
        <div class="row">
          <div class="col-6">
            <ol>
              <li>
                Follow the setup instruction in
                <a href="https://github.com/Morris88826/HAA_3D-T">here</a> to
                install the annotation tool.
              </li>
              <li>
                In the annotating page, (1) shows the annotating canvas. Users
                can use mouse scroll and drag to move the frame into the wanted
                position. Click [Reset Zoom] button on the right to go back to
                the default.
              </li>

              <li>
                To change the frame, use the bar below (2), or press (z) or (x)
                on your keyboard to go to the prev/next frame. Scroll the bar
                quickly for a video-like preview.
              </li>

              <li>
                Users can press (3) to load preliminary prediction of the joints
                from Alphapose. The predicted skeleton will be processed to
                Evoskeleton format. If the alphapose information doesn't exist,
                it will run the AlphaPose network to generate the info file
                (make sure that your device has cuda).
              </li>

              <li>
                To label, you can press [L] on your keyboard to start labeling
                17 joints. You can also use your keyboard to label a single
                joint. keys are [4],[5],[q-u], [a-j],[v]. You can use the image
                on the right (4) for the guide.
              </li>
              <li>
                The tool supports the linear interpolation method by click (5).
                Users can simply select the two frames the way, and the tool
                will perform interpolation for the joints' position in the
                intermediate frame.
              </li>
              <li>
                Users can monitor the generated 3D joints' position in (7)
                real-time and correct the corresponding 2D position to increase
                the accuracy.
              </li>
              <li>
                More information can also be found in
                <a href="https://github.com/Morris88826/HAA_3D-T">here</a>.
              </li>
            </ol>
          </div>

          <div class="col-6" style="margin: auto">
            <img
              src="../assets/annotation_tool.png"
              alt="../assets/annotation_tool.png"
              style="width: 100%"
            />
          </div>
        </div>
      </div>

      <br />
      <br/>
      <h1>Demo</h1>
      <p>Here we also provide a demo video for using the annotation tool.</p>
      <div style="text-align: center">
        <video controls style="width: 100%">
          <source :src="require('@/assets/demo.mp4')" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>
      <br/>
      <br/>
      <h1>Further Improvements</h1>
      <ul>
          <li>Working on the release a web version annotation tool so that users don't need to setup locally.</li>
          <li>Introduce a better interpolation model.</li>
      </ul>
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "AnnotationTool",
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
