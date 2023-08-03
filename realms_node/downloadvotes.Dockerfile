# Set the base image to Node.js 20.4.0
FROM node:20.4.0

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package.json package-lock.json ./

# Install npm dependencies
RUN npm install

# Copy all the .mjs files to the container
COPY *.mjs ./

# Copy the output_proposals_2023_8_3 directory to the container
COPY output_proposals_2023_8_3 ./output_proposals_2023_8_3

# Start your application (replace 'your_start_command' with the actual command to start your Node.js application)
CMD [ "node", "downloadVotes.mjs" ]
