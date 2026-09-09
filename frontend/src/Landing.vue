<template>
	<div class="bg-white px-3 overflow-clip flex flex-col gap-2">
		<div class="h-screen flex flex-col justify-center items-start text-white w-full space"
			bg-radial-[at_50%_150%] from-stone-800 to-black relative>
			<img src="/strokes.svg" class="absolute w-[80vw] self-center" />
			<h1 class="text-[22.5vw] tracking-[5vw] sora font-black ml-[5vw] self-center leading-tight z-80">SYFU</h1>
			<div class="px-[10vw] flex flex-col gap-3">
				<h2 class="text-4xl">Take control of your time.</h2>
				<button @click="go" class="text-2xl font-black text-black px-5 py-2 bg-white w-fit rounded-none">Get Started</button>
			</div>
		</div>
		<div>hellow world</div>
	</div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
const go = () => router.push('/dashboard');
</script>