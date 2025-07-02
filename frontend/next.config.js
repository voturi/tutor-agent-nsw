/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverActions: {
      bodySizeLimit: '10mb',
    },
  },
  webpack: (config) => {
    config.resolve.alias.canvas = false;
    config.resolve.alias.encoding = false;
    // PDF.js worker configuration
    config.resolve.alias['pdfjs-dist/build/pdf.worker.min.js'] = 'pdfjs-dist/build/pdf.worker.min.mjs';
    return config;
  },
};

module.exports = nextConfig;
