import Vue from "vue";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";

// only import the icons which are used
import {
  faCog,
  faInfoCircle,
  faEdit,
  faTrashAlt,
  faRetweet,
  faPlayCircle,
  faPauseCircle,
  faSyncAlt,
  faPlusCircle,
  faSave,
  faCogs,
  faLayerGroup,
} from "@fortawesome/free-solid-svg-icons";

library.add(
  faCog,
  faInfoCircle,
  faEdit,
  faTrashAlt,
  faRetweet,
  faPlayCircle,
  faPauseCircle,
  faSyncAlt,
  faPlusCircle,
  faSave,
  faCogs,
  faLayerGroup
);

Vue.component("font-awesome-icon", FontAwesomeIcon);
