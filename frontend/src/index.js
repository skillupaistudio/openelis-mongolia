import "@formatjs/intl-numberformat/polyfill.js";
import "@formatjs/intl-numberformat/locale-data/en.js";
import "@formatjs/intl-numberformat/locale-data/mn.js";
import "@formatjs/intl-datetimeformat/polyfill.js";
import "@formatjs/intl-datetimeformat/add-all-tz.js";
import "@formatjs/intl-datetimeformat/locale-data/en.js";
import "@formatjs/intl-datetimeformat/locale-data/mn.js";
import "@formatjs/intl-relativetimeformat/polyfill.js";
import "@formatjs/intl-relativetimeformat/locale-data/en.js";
import "@formatjs/intl-relativetimeformat/locale-data/mn.js";
import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import * as ServiceWorker from "./serviceWorkerRegistration";

ServiceWorker.unregisterServiceWorker();

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root"),
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
