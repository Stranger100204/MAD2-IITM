<template>

<Layout>

    <template #sidebar>
        <TrekkerSidebar />
    </template>


    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Browse Treks</h2>
    </div>

    <!-- Alerts -->
    <div v-if="error" class="alert alert-danger alert-dismissible">
        {{ error }}
        <button class="btn-close" @click="error = ''"></button>
    </div>

    <div v-if="bookingSuccess" class="alert alert-success alert-dismissible">
        {{ bookingSuccess }}
        <button class="btn-close" @click="bookingSuccess = ''"></button>
    </div>

    <!-- Filters -->
    <div class="card mb-4">
        <div class="card-body">
            <div class="row g-2">
                <div class="col-md-4">
                    <input
                        v-model="filters.q"
                        class="form-control"
                        placeholder="Search trek name..."
                        @keyup.enter="search"
                    >
                </div>
                <div class="col-md-3">
                    <input
                        v-model="filters.location"
                        class="form-control"
                        placeholder="Location..."
                        @keyup.enter="search"
                    >
                </div>
                <div class="col-md-2">
                    <select v-model="filters.difficulty" class="form-select">
                        <option value="">All Difficulties</option>
                        <option>EASY</option>
                        <option>MODERATE</option>
                        <option>HARD</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <input
                        v-model="filters.duration"
                        type="number"
                        class="form-control"
                        placeholder="Max days"
                        min="1"
                    >
                </div>
                <div class="col-md-1 d-flex gap-1">
                    <button class="btn btn-success w-100" @click="search" :disabled="searching">
                        <span v-if="searching">...</span>
                        <span v-else>🔍</span>
                    </button>
                    <button class="btn btn-outline-secondary w-100" @click="clearFilters" title="Reset">✕</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="mt-2">Loading treks...</p>
    </div>

    <!-- Treks Grid -->
    <div v-if="!loading">

        <div class="row">

            <div v-for="trek in treks" :key="trek.id" class="col-md-6 mb-3">

                <div class="card h-100">

                    <div class="card-body">

                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h5 class="card-title mb-0">{{ trek.name }}</h5>
                            <span :class="difficultyBadge(trek.difficulty)">{{ trek.difficulty }}</span>
                        </div>

                        <p class="text-muted small mb-1">📍 {{ trek.location }}</p>
                        <p class="text-muted small mb-1">📅 {{ trek.duration_days }} days &nbsp;|&nbsp; 🎫 Available: {{ trek.available_slots }} / Total: {{ trek.total_slots }} slots</p>
                        <p class="text-muted small mb-2">🗓 {{ trek.start_date }} → {{ trek.end_date }}</p>

                        <p v-if="trek.description" class="small text-secondary mb-3">{{ trek.description }}</p>

                    </div>

                    <div class="card-footer d-flex justify-content-between align-items-center">
                        <span :class="statusBadge(trek.status)">{{ trek.status }}</span>
                        <button
                            class="btn btn-success btn-sm"
                            @click="bookTrek(trek)"
                            :disabled="!canBook(trek) || booking === trek.id"
                        >
                            <span v-if="booking === trek.id">Booking...</span>
                            <span v-else-if="trek.status !== 'OPEN'">{{ trek.status }}</span>
                            <span v-else-if="trek.available_slots === 0">Full</span>
                            <span v-else-if="bookedIds.has(trek.id)">Already Booked</span>
                            <span v-else>Book Now</span>
                        </button>
                    </div>

                </div>

            </div>

        </div>

        <!-- Empty state -->
        <div v-if="treks.length === 0" class="text-center text-muted py-5">
            <p>No treks found. Try different filters.</p>
        </div>

    </div>

</Layout>

</template>

<script setup>

import { ref, reactive, onMounted } from "vue";
import { RouterLink } from "vue-router";
import Layout from "../../components/common/Layout.vue";
import TrekkerSidebar from "../../components/trekker/TrekkerSidebar.vue";
import api from "../../services/api";

const treks = ref([]);
const bookedIds = ref(new Set());
const loading = ref(true);
const searching = ref(false);
const booking = ref(null);
const error = ref("");
const bookingSuccess = ref("");

const filters = reactive({
    q: "",
    location: "",
    difficulty: "",
    duration: ""
});

function difficultyBadge(difficulty) {
    if (difficulty === "EASY") return "badge bg-success";
    if (difficulty === "MODERATE") return "badge bg-warning text-dark";
    return "badge bg-danger";
}

function statusBadge(status) {
    const map = {
        PENDING: "badge bg-secondary",
        APPROVED: "badge bg-info text-dark",
        OPEN: "badge bg-success",
        CLOSED: "badge bg-warning text-dark",
        COMPLETED: "badge bg-primary"
    };
    return map[status] || "badge bg-secondary";
}

function canBook(trek) {
    return trek.status === "OPEN" &&
        trek.available_slots > 0 &&
        !bookedIds.value.has(trek.id);
}

async function loadTreks() {

    loading.value = true;

    try {
        const res = await api.get("/trekker/treks");
        treks.value = res.data.treks;
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to load treks.";
    }
    finally {
        loading.value = false;
    }

}

async function loadBookedIds() {

    try {
        const res = await api.get("/trekker/bookings");
        const bookings = res.data.bookings;
        // Each booking from get_booking_history has trek_id as a top-level field
        bookedIds.value = new Set(
            bookings
                .filter(b => b.status === "BOOKED")
                .map(b => b.trek_id)
        );
    }
    catch { /* silent */ }

}

async function search() {

    searching.value = true;
    error.value = "";

    // Build params (only include non-empty)
    const params = {};
    if (filters.q) params.q = filters.q;
    if (filters.location) params.location = filters.location;
    if (filters.difficulty) params.difficulty = filters.difficulty;
    if (filters.duration) params.duration = filters.duration;

    try {
        const res = await api.get("/trekker/treks/search", { params });
        treks.value = res.data.treks;
    }
    catch (err) {
        error.value = err.response?.data?.error || "Search failed.";
    }
    finally {
        searching.value = false;
    }

}

async function clearFilters() {

    filters.q = "";
    filters.location = "";
    filters.difficulty = "";
    filters.duration = "";
    await loadTreks();

}

async function bookTrek(trek) {

    booking.value = trek.id;
    error.value = "";
    bookingSuccess.value = "";

    try {
        await api.post(`/trekker/treks/${trek.id}/book`);
        bookingSuccess.value = `"${trek.name}" booked successfully!`;
        bookedIds.value.add(trek.id);
        trek.available_slots--;
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to book trek.";
    }
    finally {
        booking.value = null;
    }

}

onMounted(async () => {
    await Promise.all([loadTreks(), loadBookedIds()]);
});

</script>
