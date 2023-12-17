import axios from "axios";

// axios.defaults.baseURL = 'https://rkdev-drf-api-3511a67bfcda.herokuapp.com/'
axios.defaults.headers.post['Content-Type'] = 'multipart/form-data'
axios.defaults.withCredentials = true

export const axiosReq = axios.create();
export const axiosRes = axios.create();