import {
  TextInput,
  Button,
  Group,
  Stack,
  Image,
  Card,
  Text,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { useState } from "react";
import axios from "axios";
import dayjs from "dayjs";

function App() {
  const POSTER_PREFIX = "https://image.tmdb.org/t/p/original";

  const [loading, setLoading] = useState(false);
  const [similarMovies, setSimilarMovies] = useState([]);
  const [collabMovies, setCollabMovies] = useState([]);

  const getCollabMovies = (query, similarMovies) => {
    var input = [];

    // Adding the query and top 2 similar movies to the array
    input.push(query);
    input.push(similarMovies[0].title);
    input.push(similarMovies[1].title);
    console.log(input);

    console.log("Sending request to get collab movies:", input);

    axios
      .get("http://127.0.0.1:5000/collab", {
        params: { query: input.toString() },
      })
      .then((res) => {
        console.log("Received collab response:", res.data);
        setCollabMovies(res.data);
      });
  };

  const handleSearch = (query) => {
    console.log("Sending query:", query);
    setLoading(true);
    axios
      .get("http://127.0.0.1:5000/search", { params: { query: query } })
      .then((res) => {
        console.log("Received response:", res.data);
        setLoading(false);
        setSimilarMovies(res.data);
        getCollabMovies(query, res.data);
      })
      .catch((err) => {
        console.log(err.response.data);
        setLoading(false);
        alert(err.response.data);
      });
  };

  const form = useForm({
    initialValues: {
      query: "",
    },

    validate: {
      query: (value) => (/^\S/.test(value) ? null : "Invalid query"),
    },
  });

  return (
    <Stack p="lg" justify="center" align="center" sx={{ width: "100%" }}>
      <div style={{ width: 80 }}>
        <Image src="https://cdn-icons-png.flaticon.com/512/2798/2798024.png" />
      </div>
      <h1 style={{ marginTop: 0 }}>Movie Recommender</h1>
      <form
        onSubmit={form.onSubmit((values) => handleSearch(values.query))}
        style={{ width: "100%", display: "flex", justifyContent: "center" }}
      >
        <Group sx={{ width: "60%" }} position="center" align="flex-start">
          <TextInput
            variant="filled"
            placeholder="Enter movie title here"
            {...form.getInputProps("query")}
            sx={{ flex: 1 }}
            disabled={loading}
          />
          <Button type="submit" loading={loading}>
            Submit
          </Button>
        </Group>
      </form>
      {similarMovies.length > 0 && (
        <h2 style={{ textAlign: "center" }}>We think you will like</h2>
      )}
      <Group position="center" align="stretch">
        {similarMovies?.map((movie) => (
          <Card shadow="sm" p="lg" radius="md" withBorders sx={{ width: 200 }}>
            <Card.Section>
              <Image
                src={POSTER_PREFIX + movie.poster_path}
                height={220}
                withPlaceholder
                placeholder={
                  <Text align="center">Movie poster unavailable</Text>
                }
              />
            </Card.Section>
            <Stack spacing="xs">
              <Text mt="md" weight={500} align="center">
                {movie.title}
              </Text>
              <Text mt="md" align="center">
                {dayjs(movie.release_date).format("MMM DD, YYYY")}
              </Text>
              <Text mt="md" align="center">
                {"Score: " + movie.score}
              </Text>
            </Stack>
          </Card>
        ))}
      </Group>
      {collabMovies.length > 0 && (
        <h2 style={{ textAlign: "center" }}>Other users like</h2>
      )}
      <Group position="center" align="stretch">
        {collabMovies?.map((movie) => (
          <Card shadow="sm" p="lg" radius="md" withBorders sx={{ width: 200 }}>
            <Card.Section>
              <Image
                src={POSTER_PREFIX + movie.poster_path}
                height={220}
                withPlaceholder
                placeholder={
                  <Text align="center">Movie poster unavailable</Text>
                }
              />
            </Card.Section>
            <Stack spacing="xs">
              <Text mt="md" weight={500} align="center">
                {movie.title}
              </Text>
              <Text mt="md" align="center">
                {dayjs(movie.release_date).format("MMM DD, YYYY")}
              </Text>
            </Stack>
          </Card>
        ))}
      </Group>
    </Stack>
  );
}

export default App;
