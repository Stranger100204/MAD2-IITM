<template>

<div class="container d-flex justify-content-center align-items-center vh-100">

    <div class="card shadow p-4" style="width:450px;">

        <h3 class="text-center mb-4">
            Trekker Registration
        </h3>

        <div class="mb-3">

            <label class="form-label">
                Name
            </label>

            <input
                v-model="name"
                class="form-control"
                type="text"
                placeholder="Enter your name"
            >

        </div>

        <div class="mb-3">

            <label class="form-label">
                Email
            </label>

            <input
                v-model="email"
                class="form-control"
                type="email"
                placeholder="Enter your email"
            >

        </div>

        <div class="mb-3">

            <label class="form-label">
                Phone
            </label>

            <input
                v-model="phone"
                class="form-control"
                type="text"
                placeholder="Enter phone number"
            >

        </div>

        <div class="mb-3">

            <label class="form-label">
                Password
            </label>

            <input
                v-model="password"
                class="form-control"
                type="password"
                placeholder="Enter password"
            >

        </div>

        <div
            v-if="error"
            class="alert alert-danger"
        >
            {{ error }}
        </div>

        <div
            v-if="success"
            class="alert alert-success"
        >
            {{ success }}
        </div>

        <button
            @click="register"
            class="btn btn-success w-100"
        >
            Register
        </button>

        <router-link
            to="/login"
            class="text-center mt-3 d-block"
        >
            Already have an account?
        </router-link>

    </div>

</div>

</template>

<script setup>

import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const router = useRouter();

const name = ref("");
const email = ref("");
const phone = ref("");
const password = ref("");

const error = ref("");
const success = ref("");

async function register(){

    error.value = "";
    success.value = "";

    try{

        await api.post(
            "/auth/register",
            {
                name: name.value,
                email: email.value,
                phone: phone.value,
                password: password.value
            }
        );

        success.value = "Registration successful.";

        setTimeout(()=>{

            router.push("/login");

        },1500);

    }

    catch(err){

        error.value =
            err.response?.data?.error ||
            "Registration failed.";

    }

}

</script>