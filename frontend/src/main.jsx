import React from "react";

import { Page } from "./Page.jsx";
import { Login } from "./pages/Login.jsx";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { createRoot } from "react-dom/client";
import { StrictMode } from "react";
import { Register } from "./pages/Register.jsx";
import { AuthProvider } from "./components/AuthContext.jsx";

const App = () => {
  const router = createBrowserRouter([
    {
      element: <Page></Page>,
      children: [
        {
          path: "/login",
          element: <Login></Login>,
        },
        {
          path: "/register",
          element: <Register></Register>,
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
    <AuthProvider>
      <App />
    </AuthProvider>
  </StrictMode>
);
