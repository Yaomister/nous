import React from "react";

import { Page } from "./page.jsx";
import { Login } from "./pages/Login.jsx";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { createRoot } from "react-dom/client";
import { StrictMode } from "react";

const App = () => {
  const router = createBrowserRouter([
    {
      element: <Page></Page>,
      children: [
        {
          path: "/login",
          element: <Login></Login>,
        },
      ],
    },
  ]);

  return (
    <div>
      <RouterProvider router={router} />
    </div>
  );
};

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);
