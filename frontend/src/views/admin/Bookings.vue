<template>

<Layout>

    <template #sidebar>
        <AdminSidebar />
    </template>


    <!-- Header -->
    <h2 class="mb-4">All Bookings</h2>

    <!-- Alerts -->
    <div v-if="error" class="alert alert-danger alert-dismissible">
        {{ error }}
        <button type="button" class="btn-close" @click="error = ''"></button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="mt-2">Loading bookings...</p>
    </div>

    <!-- Summary cards -->
    <div v-if="!loading" class="row mb-4">
        <div class="col-md-3">
            <div class="card shadow-sm text-center">
                <div class="card-body">
                    <h6>Total Bookings</h6>
                    <h2>{{ bookings.length }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-sm text-center">
                <div class="card-body">
                    <h6>Booked</h6>
                    <h2 class="text-success">{{ bookings.filter(b => b.status === 'BOOKED').length }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-sm text-center">
                <div class="card-body">
                    <h6>Cancelled</h6>
                    <h2 class="text-danger">{{ bookings.filter(b => b.status === 'CANCELLED').length }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-sm text-center">
                <div class="card-body">
                    <h6>Completed</h6>
                    <h2 class="text-primary">{{ bookings.filter(b => b.status === 'COMPLETED').length }}</h2>
                </div>
            </div>
        </div>
    </div>

    <!-- Bookings Table -->
    <table v-if="!loading" class="table table-bordered table-hover">

        <thead class="table-success">
            <tr>
                <th>#</th>
                <th>Trekker</th>
                <th>Trek</th>
                <th>Booking Date</th>
                <th>Status</th>
            </tr>
        </thead>

        <tbody>

            <tr v-for="booking in bookings" :key="booking.id">
                <td>{{ booking.id }}</td>
                <td>
                    <div>{{ booking.user?.name }}</div>
                    <small class="text-muted">{{ booking.user?.email }}</small>
                </td>
                <td>
                    <div>{{ booking.trek?.name }}</div>
                    <small class="text-muted">{{ booking.trek?.location }}</small>
                </td>
                <td>{{ formatDate(booking.booking_date) }}</td>
                <td>
                    <span :class="statusBadge(booking.status)">{{ booking.status }}</span>
                </td>
            </tr>

            <tr v-if="bookings.length === 0">
                <td colspan="5" class="text-center text-muted py-4">No bookings found.</td>
            </tr>

        </tbody>

    </table>

</Layout>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { RouterLink } from "vue-router";
import Layout from "../../components/common/Layout.vue";
import AdminSidebar from "../../components/admin/AdminSidebar.vue";
import api from "../../services/api";

const bookings = ref([]);
const loading = ref(true);
const error = ref("");

function statusBadge(status) {
    if (status === "BOOKED") return "badge bg-success";
    if (status === "CANCELLED") return "badge bg-danger";
    if (status === "COMPLETED") return "badge bg-primary";
    return "badge bg-secondary";
}

function formatDate(iso) {
    if (!iso) return "—";
    return new Date(iso).toLocaleString();
}

async function loadBookings() {

    loading.value = true;

    try {
        const res = await api.get("/admin/bookings");
        bookings.value = res.data.bookings;
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to load bookings.";
    }
    finally {
        loading.value = false;
    }

}

onMounted(loadBookings);

</script>
