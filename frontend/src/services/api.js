/**
 * API Service for CropGuard Backend
 */
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Analysis API
export const runAnalysis = async (bbox, areaKm2, clientId, clientSecret) => {
    const response = await api.post('/analysis/run', {
        bbox,
        area_km2: areaKm2,
        client_id: clientId,
        client_secret: clientSecret,
    });
    return response.data;
};

// Demo API
export const loadDemoScenario = async () => {
    const response = await api.get('/demo/scenario');
    return response.data;
};

// Fields API
export const getAllFields = async () => {
    const response = await api.get('/fields');
    return response.data;
};

export const saveField = async (name, bbox, aiResults, detectedCrop) => {
    const response = await api.post('/fields', {
        name,
        bbox,
        ai_results: aiResults,
        detected_crop: detectedCrop,
    });
    return response.data;
};

export const deleteField = async (fieldName) => {
    const response = await api.delete(`/fields/${fieldName}`);
    return response.data;
};

export const getFieldBbox = async (fieldName) => {
    const response = await api.get(`/fields/${fieldName}/bbox`);
    return response.data;
};

// Reports API
export const generatePDFReport = async (aiResults, bboxInfo, classification, ndviMap, detectedCrop, language = 'en') => {
    const response = await api.post('/reports/generate', {
        ai_results: aiResults,
        bbox_info: bboxInfo,
        classification,
        ndvi_map: ndviMap,
        detected_crop: detectedCrop,
        language,
    }, {
        responseType: 'blob',
    });

    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `CropGuard_Report_${Date.now()}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();

    return response.data;
};

export default api;
