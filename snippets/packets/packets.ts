import { Name, Interest, Data } from '@ndn/packet';
import { toUtf8 } from '@ndn/util';

// Create an NDN name from a URI string
const name = new Name('/edu/ucla/cs/118/notes');

// Create an Interest packet with this name
const interest = new Interest(name);

// Set the Interest packet's InterestLifetime to 5 seconds
interest.lifetime = 5000;

// Create a Data packet with the same name
const data = new Data(name);

// Set the Data packet's content to "Hello, NDN!"
data.content = toUtf8('Hello, NDN!');
