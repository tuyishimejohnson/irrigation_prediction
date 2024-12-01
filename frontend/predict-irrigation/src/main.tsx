import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import DefaultLayout from "./defaultLayout.tsx";
import Home from "./home.tsx";
import Contacts from "./contacts.tsx";
import Dashboard from "./solution.tsx";
import About from "./about.tsx";
import Predict from "./predict.tsx";

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
        path: "/about",
        element: <About />,
      },
      {
        path: "/solution",
        element: <Dashboard />,
      },

      {
        path: "/predict",
        element: <Predict />,
      },
      {
        path: "/contacts",
        element: <Contacts />,
      },
    ],
  },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);

