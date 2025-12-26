import React from "react";

import { Page } from "./Page.jsx";
import { Login } from "./pages/Login.jsx";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { createRoot } from "react-dom/client";
import { StrictMode } from "react";
import { Register } from "./pages/Register.jsx";
import { AuthProvider, useAuth } from "./components/AuthContext.jsx";
import { Recover } from "./pages/Recover.jsx";
import { ResetPassword } from "./pages/ResetPassword.jsx";
import { BookDetails } from "./pages/BookDetails.jsx";
import { Explore } from "./pages/Explore.jsx";
import { PageNotFound } from "./pages/PageNotFound.jsx";
import { Home } from "./pages/Home.jsx";

const ProtectRoute = ({ children }) => {
  const { user } = useAuth();
  if (user) return children;
  return <Navigate to="/" replace />;
};

const App = () => {
  const router = createBrowserRouter([
    {
      element: <Page></Page>,
      children: [
        {
          path: "/",
          element: <Home></Home>,
        },
        {
          path: "/login",
          element: <Login></Login>,
        },
        {
          path: "/register",
          element: <Register></Register>,
        },
        {
          path: "/recover",
          element: <Recover></Recover>,
        },
        {
          path: "/reset-password/:token",
          element: <ResetPassword></ResetPassword>,
        },

        {
          path: "/book/:id",
          element: (
            <ProtectRoute>
              <BookDetails />
            </ProtectRoute>
          ),
        },

        {
          path: "/explore",
          element: <Explore></Explore>,
        },

        {
          path: "/*",
          element: <PageNotFound></PageNotFound>,
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
