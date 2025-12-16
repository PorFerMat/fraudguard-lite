# Use an official Node runtime as a parent image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json first (for better caching)
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the frontend application code
COPY . .

# Build the React app for production (if you want to serve the static build)
# RUN npm run build

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Command to run the development server
CMD ["npm", "start"]