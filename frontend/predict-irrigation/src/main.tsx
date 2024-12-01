import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import DefaultLayout from "./defaultLayout.tsx";
import Home from "./home.tsx";
import Retrain from "./retrain.tsx";
import Results from "./results.tsx";
import IrrigationPrediction from "./components/IrrigationPrediction.tsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <DefaultLayout />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "/IrrigationPrediction",
        element: <IrrigationPrediction />,
      },
      {
        path: "/retrain",
        element: <Retrain />,
      },
      {
        path: "/results",
        element: <Results />,
      },
    ],
  },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
