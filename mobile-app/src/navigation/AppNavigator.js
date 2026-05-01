/**
 * App navigation configuration
 */
import { createStackNavigator } from '@react-navigation/stack';
import { SCREENS } from '../constants';

const Stack = createStackNavigator();

// Import screens (these should be created in the screens directory)
// import HomeScreen from '../screens/HomeScreen';
// import ResultScreen from '../screens/ResultScreen';

export default function AppNavigator() {
  return (
    <Stack.Navigator
      initialRouteName={SCREENS.HOME}
      screenOptions={{
        headerStyle: {
          backgroundColor: '#4CAF50',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}
    >
      {/* <Stack.Screen 
        name={SCREENS.HOME} 
        component={HomeScreen}
        options={{ title: 'Plant Disease Detection' }}
      />
      <Stack.Screen 
        name={SCREENS.RESULT} 
        component={ResultScreen}
        options={{ title: 'Detection Result' }}
      /> */}
    </Stack.Navigator>
  );
}
