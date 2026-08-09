<template>

<div class="container d-flex justify-content-center align-items-center vh-100">

    <div class="card shadow p-4" style="width:400px;">

        <h3 class="text-center mb-4">
            Login
        </h3>

        <div class="mb-3">
            <label class="form-label">Email</label>

            <input
                v-model="email"
                type="email"
                class="form-control"
                placeholder="Enter email"
            >
        </div>

        <div class="mb-3">
            <label class="form-label">Password</label>

            <input
                v-model="password"
                type="password"
                class="form-control"
                placeholder="Enter password"
            >
        </div>

        <div
            v-if="error"
            class="alert alert-danger"
        >
            {{ error }}
        </div>

        <button
            class="btn btn-success w-100"
            @click="login"
        >
            Login
        </button>

        <router-link
            to="/register"
            class="text-center mt-3 d-block"
        >
            Create New Account
        </router-link>

    </div>

</div>

</template>

<script setup>

import { ref } from "vue";
import { useRouter } from "vue-router";

import api from "../services/api";
import { saveToken, saveRole } from "../utils/auth";

const router = useRouter();

const email = ref("");
const password = ref("");
const error = ref("");

async function login(){

    error.value = "";

    try{

        const response = await api.post(
            "/auth/login",
            {
                email: email.value,
                password: password.value
            }
        );

        saveToken(response.data.access_token);

        saveRole(response.data.user.role);

        const role = response.data.user.role;

        if (role === "ADMIN") {

            router.push("/admin/dashboard");

        }
        else if (role === "STAFF") {

            router.push("/staff/dashboard");

        }
        else {

            router.push("/trekker/dashboard");

        }

    }
    catch(err){

        console.log(err);

        error.value =
            err.response?.data?.error ||
            "Login failed.";

    }

}

</script>