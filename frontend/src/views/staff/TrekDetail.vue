<template>

<Layout>

    <template #sidebar>
        <StaffSidebar />
    </template>


    <!-- Back link -->
    <div class="mb-3">
        <RouterLink to="/staff/treks" class="btn btn-outline-secondary btn-sm">
            ← Back to Treks
        </RouterLink>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="mt-2">Loading trek details...</p>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="actionError" class="alert alert-danger alert-dismissible">
        {{ actionError }}
        <button class="btn-close" @click="actionError = ''"></button>
    </div>
    <div v-if="actionSuccess" class="alert alert-success alert-dismissible">
        {{ actionSuccess }}
        <button class="btn-close" @click="actionSuccess = ''"></button>
    </div>

    <!-- Trek Detail -->
    <div v-if="!loading && trek">

        <!-- Trek Info Card -->
        <div class="card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h4 class="mb-0">{{ trek.name }}</h4>
                <span :class="statusBadge(trek.status)">{{ trek.status }}</span>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        <p><strong>Location:</strong> {{ trek.location }}</p>
                        <p><strong>Difficulty:</strong>
                            <span :class="difficultyBadge(trek.difficulty)">{{ trek.difficulty }}</span>
                        </p>
                    </div>
                    <div class="col-md-4">
                        <p><strong>Duration:</strong> {{ trek.duration_days }} days</p>
                        <p><strong>Slots:</strong> {{ trek.available_slots }} / {{ trek.total_slots }}</p>
                    </div>
                    <div class="col-md-4">
                        <p><strong>Start Date:</strong> {{ trek.start_date }}</p>
                        <p><strong>End Date:</strong> {{ trek.end_date }}</p>
                    </div>
                </div>
                <p v-if="trek.description"><strong>Description:</strong> {{ trek.description }}</p>
            </div>
        </div>

        <!-- Actions Card -->
        <div class="card mb-4">
            <div class="card-header fw-bold">Manage Trek</div>
            <div class="card-body">
                <div class="row g-3 align-items-end">

                    <!-- Update Status -->
                    <div class="col-md-4">
                        <label class="form-label">Update Status</label>
                        <select v-model="newStatus" class="form-select" :disabled="trek.status === 'COMPLETED'">
                            <option value="OPEN">OPEN</option>
                            <option value="CLOSED">CLOSED</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <button
                            class="btn btn-primary w-100"
                            @click="updateStatus"
                            :disabled="updatingStatus || trek.status === 'COMPLETED'"
                        >
                            <span v-if="updatingStatus">Updating...</span>
                            <span v-else>Update Status</span>
                        </button>
                    </div>

                    <!-- Complete Trek -->
                    <div class="col-md-5">
                        <button
                            class="btn btn-danger w-100"
                            @click="completeTrek"
                            :disabled="completing || trek.status === 'COMPLETED'"
                        >
                            <span v-if="completing">Processing...</span>
                            <span v-else>✅ Mark Trek as Completed</span>
                        </button>
                        <small v-if="trek.status === 'COMPLETED'" class="text-muted">Trek is already completed.</small>
                    </div>

                </div>
            </div>
        </div>

        <!-- Participants Table -->
        <h5 class="mb-3">Participants ({{ participants.length }})</h5>

        <div v-if="loadingParticipants" class="text-center py-3">
            <div class="spinner-border spinner-border-sm text-success" role="status"></div>
        </div>

        <table v-else class="table table-bordered table-hover">
            <thead class="table-success">
                <tr>
                    <th>#</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Booking Date</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(p, idx) in participants" :key="p.booking_id">
                    <td>{{ idx + 1 }}</td>
                    <td>{{ p.user?.name }}</td>
                    <td>{{ p.user?.email }}</td>
                    <td>{{ p.user?.phone || '—' }}</td>
                    <td>{{ formatDate(p.booking_date) }}</td>
                    <td>
                        <span :class="bookingStatusBadge(p.status)">{{ p.status }}</span>
                    </td>
                </tr>
                <tr v-if="participants.length === 0">
                    <td colspan="6" class="text-center text-muted py-4">No participants yet.</td>
                </tr>
            </tbody>
        </table>

    </div>

</Layout>

</template>

<script setup>

import { ref, onMounted } from "vue";
import { RouterLink, useRoute } from "vue-router";
import Layout from "../../components/common/Layout.vue";
import StaffSidebar from "../../components/staff/StaffSidebar.vue";
import api from "../../services/api";

const route = useRoute();
const trekId = route.params.id;

const trek = ref(null);
const participants = ref([]);
const loading = ref(true);
const loadingParticipants = ref(true);
const error = ref("");
const actionError = ref("");
const actionSuccess = ref("");
const newStatus = ref("OPEN");
const updatingStatus = ref(false);
const completing = ref(false);

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

function bookingStatusBadge(status) {
    if (status === "BOOKED") return "badge bg-success";
    if (status === "CANCELLED") return "badge bg-danger";
    if (status === "COMPLETED") return "badge bg-primary";
    return "badge bg-secondary";
}

function formatDate(iso) {
    if (!iso) return "—";
    return new Date(iso).toLocaleDateString();
}

async function loadTrek() {

    loading.value = true;

    try {
        const res = await api.get(`/staff/treks/${trekId}`);
        trek.value = res.data.trek;
        newStatus.value = trek.value.status === "COMPLETED" ? "OPEN" : trek.value.status;
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to load trek details.";
    }
    finally {
        loading.value = false;
    }

}

async function loadParticipants() {

    loadingParticipants.value = true;

    try {
        const res = await api.get(`/staff/treks/${trekId}/participants`);
        participants.value = res.data.participants;
    }
    catch { /* silent */ }
    finally {
        loadingParticipants.value = false;
    }

}

async function updateStatus() {

    actionError.value = "";
    updatingStatus.value = true;

    try {
        const res = await api.put(`/staff/treks/${trekId}/status`, { status: newStatus.value });
        trek.value = res.data.trek;
        actionSuccess.value = "Trek status updated successfully.";
    }
    catch (err) {
        actionError.value = err.response?.data?.error || "Failed to update status.";
    }
    finally {
        updatingStatus.value = false;
    }

}

async function completeTrek() {

    if (!confirm("Mark this trek as COMPLETED? This action cannot be undone.")) return;

    actionError.value = "";
    completing.value = true;

    try {
        const res = await api.put(`/staff/treks/${trekId}/complete`);
        trek.value = res.data.trek;
        actionSuccess.value = "Trek marked as completed.";
        await loadParticipants();
    }
    catch (err) {
        actionError.value = err.response?.data?.error || "Failed to complete trek.";
    }
    finally {
        completing.value = false;
    }

}

onMounted(async () => {
    await Promise.all([loadTrek(), loadParticipants()]);
});

</script>
