<template>

<div>

    <!-- Navbar -->

    <nav class="navbar navbar-dark bg-success">

        <div class="container-fluid">

            <span class="navbar-brand mb-0 h1">

                🏔 Trek Management System

            </span>

            <button
                class="btn btn-light btn-sm"
                @click="logoutUser"
            >

                Logout

            </button>

        </div>

    </nav>

    <div class="container-fluid">

        <div class="row">

            <!-- Sidebar -->

            <div
                class="col-md-2 bg-light vh-100 border-end pt-3"
            >

                <slot name="sidebar"></slot>

            </div>

            <!-- Main Content -->

            <div
                class="col-md-10 p-4"
            >

                <slot></slot>

            </div>

        </div>

    </div>

</div>

</template>

<script setup>

import { useRouter } from "vue-router";

import { logout } from "../../utils/auth";

const router = useRouter();

function logoutUser(){

    logout();

    router.push("/login");

}

</script>