import { createBrowserRouter } from "react-router";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Transaction from "./pages/Transaction";
import Budget from "./pages/Budget";
import Stats from "./pages/Stats";
import Profile from "./pages/Profile";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Login,
  },
  {
    path: "/register",
    Component: Register,
  },
  {
    path: "/dashboard",
    Component: Dashboard,
  },
  {
    path: "/transaction",
    Component: Transaction,
  },
  {
    path: "/transaction/:id",
    Component: Transaction,
  },
  {
    path: "/budget",
    Component: Budget,
  },
  {
    path: "/stats",
    Component: Stats,
  },
  {
    path: "/profile",
    Component: Profile,
  },
]);
