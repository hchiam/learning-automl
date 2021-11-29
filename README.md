# Learning AutoML [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://github.com/hchiam/learning-template/blob/main/LICENSE)

Just one of the things I'm learning. https://github.com/hchiam/learning

Let AutoML figure out how to train your model, like the hyperparameters, and then export/deploy that model. The web interface can even export explainer visualizations ("Explainable AI") into Google Storage buckets.

Live demo: https://learning-automl-test.surge.sh/

## Tutorial I'm following

https://towardsdatascience.com/getting-started-with-automl-vision-alpha-ba769121235c?gi=50d5dbdc9899 It's already starting to get out of date, but shows the main ideas. The notes below help fill in some of the current steps I had to do to get a running demo to actually work.

## Things to install locally

https://ffmpeg.org/download.html or just a CLI command like `brew install ffmpeg` (and check that it's installed by running `ffmpeg -version`, yes with just one dash)

https://cloud.google.com/storage/docs/gsutil_install or just one of the CLI commands like `pip3 install gsutil` (and check that it's installed by running `gsutil --version`) and you might want to read https://cloud.google.com/storage/docs/quickstart-gsutil

## Google Cloud Platform setup

Create a project on https://console.cloud.google.com/ and then enable billing for that project (make sure it's linked), and then open https://cloud.google.com/automl and choose AutoML Vision and enable adding Vertex AI APO (aiplatform.googleapis.com) to that project. (As of this writing, AutoML Vision is now part of the new Vertex AI.) The key pages are "Datasets", "Training", and "Models" (for model endpoints).

Vertex AI dashboard: https://console.cloud.google.com/vertex-ai?project=YOUR-PROJECT-ID

Example: https://console.cloud.google.com/vertex-ai?project=learning-automl-test

## CLI data prep setup

Label by folders, summarize in CSV, and upload for ML training:

```sh
ffmpeg -i all_data/bike/bike.gif all_data/bike/bike%03d.jpg

ffmpeg -i all_data/chair_blue/chair_blue.gif all_data/chair_blue/chair_blue%03d.jpg

ffmpeg -i all_data/chair_wood/chair_wood.mp4 all_data/chair_wood/chair_wood_%03d.jpg

gsutil config
# (go to URL, paste the auth code, and enter the project-id of the project you set up earlier)

# name your Google Storage bucket something like learning-automl-test
gsutil mb -b on -l us-central1 gs://learning-automl-test/

# then fill in a folder inside that bucket
gsutil -m cp -r all_data gs://learning-automl-test/dataset

pip3 install pandas
py data_prep.py
gsutil cp all_data.csv gs://learning-automl-test/dataset/
```

## Do the actual dataset import, training, and model endpoint setup in the project

Now in the browser UI in your project in Google Cloud Platform, click on "CREATE DATA SET", open a data set, and import the .csv file you uploaded earlier to Cloud Storage. You'll likely need to wait a few minutes for a completion notification email.

Go to the Training section --> Create. There's lots of options (I chose a regular Training job, with [AutoML Edge](https://cloud.google.com/vertex-ai/docs/training/automl-edge-console)). Or just click on "TRAIN NEW MODEL" if you're already inside a dataset's browse tab. Or even faster, just go to https://model.new/. Again, wait for a completion notification email.

Go to the Models section or the Endpoints section to deploy and test it out! You can create an endpoint for online predictions, or export the model, especially for the edge type of AutoML model (see [how to export AutoML Edge models](https://cloud.google.com/vertex-ai/docs/export/export-edge-model) and then for example [how to load a Tensorflow.js model for Node.js](https://www.tensorflow.org/js/guide/save_load#loading_a_tfmodel)).

For example, in your model, go to the "DEPLOY AND TEST" tab. Then you can select to deploy to an endpoint, or (like me) deploy as a TensorFlow.js model package to Google Cloud Storage (I chose to put it in the top level of my bucket: `gs://learning-automl-test`).

It might take a moment for the model files to export to your `gs` bucket. Check that the model files are ready:

```sh
gsutil ls gs://learning-automl-test
# you'll see the model folder listed when it's ready:
# gs://learning-automl-test/dataset/
# gs://learning-automl-test/model-#######
```

Look into the sub-directories so you can run something like the following:

```sh
# gsutil cp gs://OUTPUT_BUCKET/model-MODEL_ID/tf-js/YYYY-MM-DDThh:mm:ss.sssZ/ ./download_dir
gsutil cp -r gs://learning-automl-test/model-6652735841347043328/tf-js/2021-11-28T20:21:28.935523Z/* model_export
```

```js
// const model = await tf.loadLayersModel("file://path/to/my-model/model.json");
const model = await tf.automl.loadImageClassification(
  "model_export/model.json" // file://path/to/my-model/model.json
);
```

And then use code like that found in `index.html`, or https://github.com/hchiam/text-similarity-test or https://codepen.io/hchiam/pen/LYYRLzz?editors=1010

And finally, to view the demo (index.html) in a browser, you could run these [`yarn`](https://github.com/hchiam/learning-yarn) commands already set up in this repo:

```sh
yarn # to install dependencies
yarn dev
# http://localhost:8000
```

Under the hood, it runs `http-server -p 8000` (I couldn't get `async` to work with [`parcel index.html`](https://github.com/hchiam/learning-parcel)).

For more info specific to AutoML Edge web app setup: https://cloud.google.com/vision/automl/docs/tensorflow-js-tutorial#write_a_small_web_app

## Evaluating your model

"Models" section > Click on your model > "EVALUATE" tab.

https://cloud.google.com/vertex-ai/docs/training/evaluating-automl-models

## [`surge`](https://github.com/hchiam/learning-surge) deploy

```sh
mkdir surge
mkdir surge/model_export
mkdir surge/all_data
mkdir surge/all_data/bike
cp model_export/model.json surge/model_export/model.json
cp model_export/dict.txt surge/model_export/dict.txt
cp model_export/group1-shard1of1.bin surge/model_export/group1-shard1of1.bin
cp all_data/bike/bike070.jpg surge/all_data/bike/bike070.jpg
cp index.html surge/index.html
cp favicon.ico surge/favicon.ico
surge surge
# surge surge https://learning-automl-test.surge.sh
```

## Even more AI/ML stuff

https://github.com/hchiam/machineLearning
