<template>
  <div>
    <input type="file" @change="uploadFile" />
  </div>
</template>

<script setup>
const uploadFile = async (e) => {
  const file = e.target.files[0];
  const formData = new FormData();
  formData.append("file", file);

  await fetch("http://localhost:8000/upload", {
    method: "POST",
    body: formData
  });
};
</script>