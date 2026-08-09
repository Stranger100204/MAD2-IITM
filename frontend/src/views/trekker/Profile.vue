<template>

<Layout>

    <template #sidebar>
        <TrekkerSidebar />
    </template>


    <!-- Header -->
    <h2 class="mb-4">My Profile</h2>

    <!-- Alerts -->
    <div v-if="error" class="alert alert-danger alert-dismissible">
        {{ error }}
        <button class="btn-close" @click="error = ''"></button>
    </div>

    <div v-if="success" class="alert alert-success alert-dismissible">
        {{ success }}
        <button class="btn-close" @click="success = ''"></button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-success" role="status"></div>
        <p class="mt-2">Loading profile...</p>
    </div>

    <!-- Profile Form -->
    <div v-if="!loading" class="row">

        <div class="col-md-6">

            <div class="card">

                <div class="card-header fw-bold">Profile Information</div>

                <div class="card-body">

                    <div class="mb-3">
                        <label class="form-label">Name</label>
                        <input v-model="form.name" class="form-control" placeholder="Your name">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input
                            :value="profile.email"
                            class="form-control"
                            disabled
                            title="Email cannot be changed"
                        >
                        <small class="text-muted">Email cannot be changed.</small>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Phone</label>
                        <input v-model="form.phone" class="form-control" placeholder="Phone number">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Role</label>
                        <input :value="profile.role" class="form-control" disabled>
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Member Since</label>
                        <input :value="formatDate(profile.created_at)" class="form-control" disabled>
                    </div>

                    <button
                        class="btn btn-success w-100"
                        @click="updateProfile"
                        :disabled="saving"
                    >
                        <span v-if="saving">Saving...</span>
                        <span v-else>Update Profile</span>
                    </button>

                </div>

            </div>

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

const profile = ref({});
const form = reactive({ name: "", phone: "" });
const loading = ref(true);
const saving = ref(false);
const error = ref("");
const success = ref("");

function formatDate(iso) {
    if (!iso) return "—";
    return new Date(iso).toLocaleDateString();
}

async function loadProfile() {

    loading.value = true;

    try {
        const res = await api.get("/trekker/profile");
        profile.value = res.data.user;
        form.name = profile.value.name || "";
        form.phone = profile.value.phone || "";
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to load profile.";
    }
    finally {
        loading.value = false;
    }

}

async function updateProfile() {

    saving.value = true;
    error.value = "";
    success.value = "";

    try {
        const res = await api.put("/trekker/profile", {
            name: form.name,
            phone: form.phone
        });

        profile.value = res.data.user;
        success.value = "Profile updated successfully.";
    }
    catch (err) {
        error.value = err.response?.data?.error || "Failed to update profile.";
    }
    finally {
        saving.value = false;
    }

}

onMounted(loadProfile);

</script>
