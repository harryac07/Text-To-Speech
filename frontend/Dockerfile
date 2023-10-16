# Use the official Node.js image as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json to the container
COPY package*.json ./

# Install app dependencies
RUN npm install
RUN npm install react-scripts@3.4.1 -g

# Copy the rest of the application code to the container
COPY . .

# Build the React app
RUN npm run build

# Expose the port your React app is running on (usually 3000)
EXPOSE 3000

# start app
CMD ["npm", "start"]