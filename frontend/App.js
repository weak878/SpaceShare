import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text } from 'react-native-paper';

export default function App() {
  return (
    <View style={styles.container}>
      <Text variant="displayLarge">Welcome to SpaceShare!</Text>
      <Text variant="bodyLarge">Share wild ideas. Create amazing code.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
