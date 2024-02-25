# Use the official Nginx image as the base image
FROM nginx:latest

# Copy nginx.conf from the current directory to the container's /etc/nginx directory
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 to the outside world
EXPOSE 81

# Command to run when the container starts
CMD ["nginx", "-g", "daemon off;"]
