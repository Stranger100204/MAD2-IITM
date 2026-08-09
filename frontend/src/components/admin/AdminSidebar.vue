<template>
<div>
    <p class="fw-semibold text-muted px-2 mb-2 small text-uppercase" style="font-size:0.7rem;letter-spacing:0.08em;">Admin Panel</p>
    <div class="sidebar-nav list-group list-group-flush">
        <RouterLink to="/admin/dashboard" class="list-group-item list-group-item-action" active-class="active">Dashboard</RouterLink>
        <RouterLink to="/admin/treks" class="list-group-item list-group-item-action" active-class="active">Treks</RouterLink>
        <RouterLink to="/admin/staff" class="list-group-item list-group-item-action" active-class="active">Staff</RouterLink>
        <RouterLink to="/admin/users" class="list-group-item list-group-item-action" active-class="active">Users</RouterLink>
        <RouterLink to="/admin/bookings" class="list-group-item list-group-item-action" active-class="active">Bookings</RouterLink>
        <RouterLink to="/admin/reports" class="list-group-item list-group-item-action" active-class="active">Reports</RouterLink>
        <RouterLink to="/admin/search" class="list-group-item list-group-item-action" active-class="active">Search</RouterLink>
    </div>
</div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>
