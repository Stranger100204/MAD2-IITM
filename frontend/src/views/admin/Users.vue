<template>

<Layout>

    <template #sidebar>
        <AdminSidebar />
    </template>


    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>User Management</h2>
        <div class="input-group" style="width: 300px;">
            <input
                v-model="searchQuery"
                class="form-control"
                placeholder="Search by name..."
                @input="filterUsers"
            >
            <span class="input-group-text">🔍</span>
        </div>
    </div>

    <!-- Alerts -->
    <div v-if="error" class="alert alert-danger alert-dismissible">
        {{ error }}
        <button type="button" class="btn-close" @click="error = ''"></button>
    </div>

    <div v-if="success" class="alert alert-success alert-dismissible">
        {{ success }}
        <button type="button" class="btn-close" @click="success = ''"></button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="mt-2">Loading users...</p>
    </div>

    <!-- Users Table -->
    <table v-if="!loading" class="table table-bordered table-hover">

        <thead class="table-success">
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Role</th>
                <th>Status</th>
                <th>Joined</th>
                <th>Actions</th>
            </tr>
        </thead>

        <tbody>

            <tr v-for="user in filteredUsers" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.phone || '—' }}</td>
                <td>
                    <span :class="roleBadge(user.role)">{{ user.role }}</span>
                </td>
                <td>
                    <span :class="user.status === 'ACTIVE' ? 'badge bg-success' : 'badge bg-danger'">
                        {{ user.status }}
                    </span>
                </td>
                <td>{{ formatDate(user.created_at) }}</td>
                <td>
                    <span v-if="user.id === 1" class="text-muted">—</span>
                    <template v-else>
                        <button
                            v-if="user.status === 'ACTIVE'"
                            class="btn btn-danger btn-sm"
                            @click="updateStatus(user, 'BLACKLISTED')"
                            :disabled="updating === user.id"
                        >
                            <span v-if="updating === user.id">...</span>
                            <span v-else>Blacklist</span>
                        </button>
                        <button
                            v-else
                            class="btn btn-success btn-sm"
                            @click="updateStatus(user, 'ACTIVE')"
                            :disabled="updating === user.id"
                        >
                            <span v-if="updating === user.id">...</span>
                            <span v-else>Activate</span>
                        </button>
                    </template>
                </td>
            </tr>

            <tr v-if="filteredUsers.length === 0">
                <td colspan="8" class="text-center text-muted py-4">No users found.</td>
            </tr>

        </tbody>

    </table>

</Layout>

</template>

<script setup>

import { ref, computed, onMounted } from "vue";
import { RouterLink } from "vue-router";
import Layout from "../../components/common/Layout.vue";
import AdminSidebar from "../../components/admin/AdminSidebar.vue";
import api from "../../services/api";

const users = ref([]);
const loading = ref(true);
const error = ref("");
const success = ref("");
const updating = ref(null);
const searchQuery = ref("");

const filteredUsers = computed(() => {

    if (!searchQuery.value.trim()) return users.value;

    const q = searchQuery.value.toLowerCase();

    return users.value.filter(u =>
        u.name?.toLowerCase().includes(q) ||
        u.email?.toLowerCase().includes(q)
    );

});

function roleBadge(role) {
    if (role === "ADMIN") return "badge bg-danger";
    if (role === "STAFF") return "badge bg-info text-dark";
    return "badge bg-secondary";
}

function formatDate(iso) {
    if (!iso) return "—";
    return new Date(iso).toLocaleDateString();
}

async function loadUsers() {

    loading.value = true;

    try {
        const res = await api.get("/admin/users");
        users.value = res.data.users;
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to load users.";
    }
    finally {
        loading.value = false;
    }

}

async function updateStatus(user, status) {

    if (!confirm(`Change status of "${user.name}" to ${status}?`)) return;

    updating.value = user.id;

    try {
        await api.put(`/admin/users/${user.id}/status`, { status });
        success.value = `User status updated to ${status}.`;
        await loadUsers();
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to update status.";
    }
    finally {
        updating.value = null;
    }

}

onMounted(loadUsers);

</script>
