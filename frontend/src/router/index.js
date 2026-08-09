import { createRouter, createWebHistory } from "vue-router";

import Landing from "../views/Landing.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";

// Admin
import AdminDashboard from "../views/admin/Dashboard.vue";
import AdminTreks from "../views/admin/Treks.vue";
import AdminStaff from "../views/admin/Staff.vue";
import AdminUsers from "../views/admin/Users.vue";
import AdminBookings from "../views/admin/Bookings.vue";
import AdminReports from "../views/admin/Reports.vue";
import AdminSearch from "../views/admin/Search.vue";

// Staff
import StaffDashboard from "../views/staff/Dashboard.vue";
import StaffTreks from "../views/staff/Treks.vue";
import StaffTrekDetail from "../views/staff/TrekDetail.vue";

// Trekker
import TrekkerDashboard from "../views/trekker/Dashboard.vue";
import TrekkerTreks from "../views/trekker/Treks.vue";
import TrekkerBookings from "../views/trekker/Bookings.vue";
import TrekkerProfile from "../views/trekker/Profile.vue";

const routes = [

    { path: "/", component: Landing },
    { path: "/login", component: Login },
    { path: "/register", component: Register },

    // Admin routes
    { path: "/admin/dashboard", component: AdminDashboard, meta: { requiresAuth: true, role: "ADMIN" } },
    { path: "/admin/treks", component: AdminTreks, meta: { requiresAuth: true, role: "ADMIN" } },
    { path: "/admin/staff", component: AdminStaff, meta: { requiresAuth: true, role: "ADMIN" } },
    { path: "/admin/users", component: AdminUsers, meta: { requiresAuth: true, role: "ADMIN" } },
    { path: "/admin/bookings", component: AdminBookings, meta: { requiresAuth: true, role: "ADMIN" } },
    { path: "/admin/reports", component: AdminReports, meta: { requiresAuth: true, role: "ADMIN" } },
    { path: "/admin/search", component: AdminSearch, meta: { requiresAuth: true, role: "ADMIN" } },

    // Staff routes
    { path: "/staff/dashboard", component: StaffDashboard, meta: { requiresAuth: true, role: "STAFF" } },
    { path: "/staff/treks", component: StaffTreks, meta: { requiresAuth: true, role: "STAFF" } },
    { path: "/staff/treks/:id", component: StaffTrekDetail, meta: { requiresAuth: true, role: "STAFF" } },

    // Trekker routes
    { path: "/trekker/dashboard", component: TrekkerDashboard, meta: { requiresAuth: true, role: "TREKKER" } },
    { path: "/trekker/treks", component: TrekkerTreks, meta: { requiresAuth: true, role: "TREKKER" } },
    { path: "/trekker/bookings", component: TrekkerBookings, meta: { requiresAuth: true, role: "TREKKER" } },
    { path: "/trekker/profile", component: TrekkerProfile, meta: { requiresAuth: true, role: "TREKKER" } },

];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {

    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    if (to.meta.requiresAuth) {

        if (!token) {
            return next("/login");
        }

        if (to.meta.role && role !== to.meta.role) {
            // Redirect to correct dashboard
            if (role === "ADMIN") return next("/admin/dashboard");
            if (role === "STAFF") return next("/staff/dashboard");
            if (role === "TREKKER") return next("/trekker/dashboard");
            return next("/login");
        }

    }

    next();

});

export default router;