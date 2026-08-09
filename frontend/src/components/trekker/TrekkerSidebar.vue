<template>
<div>
    <p class="fw-semibold text-muted px-2 mb-2 small text-uppercase" style="font-size:0.7rem;letter-spacing:0.08em;">Trekker Panel</p>
    <div class="sidebar-nav list-group list-group-flush">
        <RouterLink to="/trekker/dashboard" class="list-group-item list-group-item-action" active-class="active">Dashboard</RouterLink>
        <RouterLink to="/trekker/treks" class="list-group-item list-group-item-action" active-class="active">Browse Treks</RouterLink>
        <RouterLink to="/trekker/bookings" class="list-group-item list-group-item-action" active-class="active">My Bookings</RouterLink>
        <RouterLink to="/trekker/profile" class="list-group-item list-group-item-action" active-class="active">Profile</RouterLink>
    </div>
</div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>
