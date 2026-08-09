<template>

<Layout>

    <template #sidebar>
        <TrekkerSidebar />
    </template>


    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>My Bookings</h2>
        <div class="d-flex gap-2">
            <button
                class="btn btn-outline-success"
                @click="exportBookings"
                :disabled="exporting"
            >
                <span v-if="exporting">Generating...</span>
                <span v-else>📥 Generate CSV</span>
            </button>
            <button
                v-if="exportReady"
                class="btn btn-success"
                @click="downloadCSV"
            >
                ⬇ Download CSV
            </button>
        </div>
    </div>

    <!-- Alerts -->
    <div v-if="error" class="alert alert-danger alert-dismissible">
        {{ error }}
        <button class="btn-close" @click="error = ''"></button>
    </div>

    <div v-if="exportMessage" class="alert alert-success alert-dismissible">
        {{ exportMessage }}
        <button class="btn-close" @click="exportMessage = ''"></button>
    </div>

    <div v-if="cancelSuccess" class="alert alert-success alert-dismissible">
        {{ cancelSuccess }}
        <button class="btn-close" @click="cancelSuccess = ''"></button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="mt-2">Loading bookings...</p>
    </div>

    <!-- Bookings Table -->
    <table v-if="!loading" class="table table-bordered table-hover">

        <thead class="table-success">
            <tr>
                <th>#</th>
                <th>Trek Name</th>
                <th>Location</th>
                <th>Booking Date</th>
                <th>Trek Status</th>
                <th>Booking Status</th>
                <th>Actions</th>
            </tr>
        </thead>

        <tbody>

            <tr v-for="booking in bookings" :key="booking.id">
                <td>{{ booking.id }}</td>
                <td>{{ booking.trek?.name }}</td>
                <td>{{ booking.trek?.location }}</td>
                <td>{{ formatDate(booking.booking_date) }}</td>
                <td>
                    <span :class="trekStatusBadge(booking.trek?.status)">{{ booking.trek?.status || '—' }}</span>
                </td>
                <td>
                    <span :class="statusBadge(booking.status)">{{ booking.status }}</span>
                </td>
                <td>
                    <button
                        v-if="booking.status === 'BOOKED' && booking.trek?.status !== 'COMPLETED'"
                        class="btn btn-danger btn-sm"
                        @click="cancelBooking(booking)"
                        :disabled="cancelling === booking.id"
                    >
                        <span v-if="cancelling === booking.id">...</span>
                        <span v-else>Cancel</span>
                    </button>
                    <span v-else class="text-muted">—</span>
                </td>
            </tr>

            <tr v-if="bookings.length === 0">
                <td colspan="7" class="text-center text-muted py-4">No bookings found. <RouterLink to="/trekker/treks">Browse Treks</RouterLink></td>
            </tr>

        </tbody>

    </table>

</Layout>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { RouterLink } from "vue-router";
import Layout from "../../components/common/Layout.vue";
import TrekkerSidebar from "../../components/trekker/TrekkerSidebar.vue";
import api from "../../services/api";

const bookings = ref([]);
const loading = ref(true);
const cancelling = ref(null);
const exporting = ref(false);
const exportReady = ref(false);
const error = ref("");
const cancelSuccess = ref("");
const exportMessage = ref("");

function statusBadge(status) {
    if (status === "BOOKED") return "badge bg-success";
    if (status === "CANCELLED") return "badge bg-danger";
    if (status === "COMPLETED") return "badge bg-primary";
    return "badge bg-secondary";
}

function trekStatusBadge(status) {
    const map = {
        PENDING: "badge bg-secondary",
        APPROVED: "badge bg-info text-dark",
        OPEN: "badge bg-success",
        CLOSED: "badge bg-warning text-dark",
        COMPLETED: "badge bg-primary"
    };
    return map[status] || "badge bg-secondary";
}

function formatDate(iso) {
    if (!iso) return "—";
    return new Date(iso).toLocaleString();
}

async function loadBookings() {

    loading.value = true;

    try {
        const res = await api.get("/trekker/bookings");
        bookings.value = res.data.bookings;
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to load bookings.";
    }
    finally {
        loading.value = false;
    }

}

async function cancelBooking(booking) {

    if (!confirm(`Cancel booking for "${booking.trek?.name}"?`)) return;

    cancelling.value = booking.id;
    error.value = "";

    try {
        await api.delete(`/trekker/bookings/${booking.id}`);
        cancelSuccess.value = "Booking cancelled successfully.";
        await loadBookings();
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to cancel booking.";
    }
    finally {
        cancelling.value = null;
    }

}

async function exportBookings() {

    exporting.value = true;
    exportMessage.value = "";
    exportReady.value = false;
    error.value = "";

    try {
        await api.post("/trekker/bookings/export");
        exportMessage.value = "CSV generated! Click the Download CSV button to save it.";
        exportReady.value = true;
    }
    catch (err) {
        error.value = err.response?.data?.error || "Export failed.";
    }
    finally {
        exporting.value = false;
    }

}

function downloadCSV() {
    const token = localStorage.getItem("token");
    fetch("http://localhost:5000/api/trekker/bookings/download", {
        headers: { "Authorization": `Bearer ${token}` }
    })
    .then(res => {
        if (!res.ok) throw new Error("Download failed");
        return res.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "my_bookings.csv";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    })
    .catch(() => {
        error.value = "Download failed. Please generate the CSV first.";
    });
}

onMounted(loadBookings);

</script>
