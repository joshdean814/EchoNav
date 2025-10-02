import sys
import os
import time
import numpy as np
import sounddevice as sd

sys.path.append(os.path.dirname(__file__))

from speaker_beep.speaker_beep import SpeakerBeep

class MockDistanceReading:
    def __init__(self, distance):
        self.distance = distance

def test_audio_system():
    """Test if the audio system is working"""
    print("Testing audio system...")
    
    try:
        duration = 0.3
        frequency = 1000
        sample_rate = 44100
        
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        
        print("Playing test tone...")
        sd.play(wave, sample_rate)
        sd.wait() 
        
        print("✓ Audio system is working!")
        return True
        
    except Exception as e:
        print(f"✗ Audio system test failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of SpeakerBeep class"""
    print("\nTesting basic SpeakerBeep functionality...")
    
    beep = SpeakerBeep()
    
    test_cases = [
        {"desc": "Very close (5cm)", "dist": 5, "expected_duration": 0.5},
        {"desc": "Close (15cm)", "dist": 15, "expected_duration": 1.5},
        {"desc": "Medium (25cm)", "dist": 25, "expected_duration": 3.0},
        {"desc": "Far (40cm)", "dist": 40, "expected_duration": 3.0},
        {"desc": "Very far (60cm)", "dist": 60, "expected_duration": None},
        {"desc": "No objects", "dist": None, "expected_duration": None},
    ]
    
    print("Testing distance to duration mapping:")
    for case in test_cases:
        if case['dist'] is None:
            objects = []
        else:
            objects = [MockDistanceReading(case['dist'])]
        
        beep.update_closest(objects)
        
        print(f"  {case['desc']}: {beep._curr_duration}s (expected: {case['expected_duration']}s)")
        
        if beep._curr_duration != case['expected_duration']:
            print(f"✗ Failed for {case['desc']}")
            return False
    
    print("✓ All distance-to-duration mappings are correct!")
    return True

def test_audio_playback():
    """Test that audio playback works without blocking"""
    print("\nTesting audio playback...")
    
    beep = SpeakerBeep()
    
    objects = [MockDistanceReading(5)]
    beep.update_closest(objects)
    
    print("Playing beep (should not block)...")
    start_time = time.time()
    
    beep.play_beep()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"play_beep() execution time: {execution_time:.3f}s")
    
    if execution_time < 0.05:  
        print("✓ Audio playback is non-blocking!")
        return True
    else:
        print("✗ Audio playback might be blocking!")
        return False

def test_backup_simulation():
    """Simulate a backup scenario with decreasing distances and actual audio"""
    print("\nSimulating backup scenario with actual audio...")
    print("You should hear beeps with increasing frequency as distance decreases")
    print("Make sure your speakers are on and volume is up!")
    
    beep = SpeakerBeep()
    
    distances = [100, 80, 60, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 2]
    
    for distance in distances:
        objects = [MockDistanceReading(distance)]
        beep.update_closest(objects)
        
        if distance >= 50:
            status = "Safe"
        elif distance >= 30:
            status = "Warning"
        elif distance >= 10:
            status = "Danger"
        else:
            status = "CRITICAL"
            
        print(f"Distance: {distance:3d}cm | Beep interval: {beep._curr_duration}s | {status}")
        
        if beep._curr_duration:
            print("  Playing beep...")
            beep.play_beep()
            time.sleep(beep._curr_duration)
        else:
            print("  No beep (safe distance)")
            time.sleep(1.0)
    
    print("✓ Backup simulation completed!")
    return True

def test_stop_functionality():
    """Test that stop_beep function works correctly"""
    print("\nTesting stop functionality...")
    
    beep = SpeakerBeep()
    
    objects = [MockDistanceReading(5)]
    beep.update_closest(objects)
    
    print("Playing beep...")
    beep.play_beep()
    
    time.sleep(0.2)
    
    print("Stopping beep...")
    beep._stop_beep()
    
    beep._stop_beep()
    
    print("✓ Stop functionality works correctly!")
    return True

def test_continuous_beeping():
    """Test continuous beeping with different distances"""
    print("\nTesting continuous beeping with different distances...")
    
    beep = SpeakerBeep()
    
    test_sequence = [
        (60, "Safe - should be silent"),
        (40, "Far - 3.0s beeps"),
        (25, "Medium - 1.5s beeps"),
        (10, "Close - 0.5s beeps"),
        (5, "Very close - 0.5s beeps"),
    ]
    
    for distance, description in test_sequence:
        print(f"\nTesting {distance}cm: {description}")
        
        objects = [MockDistanceReading(distance)]
        beep.update_closest(objects)
        
        print(f"  Beep interval: {beep._curr_duration}s")
        
        if beep._curr_duration:
            for i in range(3):
                print(f"  Beep {i+1}...")
                beep.play_beep()
                time.sleep(beep._curr_duration)
        else:
            print("  No beeps (as expected)")
            time.sleep(2.0)
    
    print("✓ Continuous beeping test completed!")
    return True

def test_constant_distance():
    """Test if beep interval remains stable when distance is constant"""
    print("\nTesting beep interval with constant distance...")
    beep = SpeakerBeep()
    constant_distance = 20  # 20cm, should result in 1.5s interval
    objects = [MockDistanceReading(constant_distance)]
    beep.update_closest(objects)
    interval = beep._curr_duration
    print(f"Distance: {constant_distance}cm | Expected interval: 1.5s | Actual interval: {interval}s")
    if interval != 1.5:
        print(f"✗ Interval incorrect, actual: {interval}s")
        return False
    print("Playing beep 3 times, interval should be consistent...")
    for i in range(3):
        print(f"  Beep {i+1}...")
        beep.play_beep()
        time.sleep(interval)
    print("✓ Beep interval is stable when distance is constant!")
    return True

def interactive_test():
    """Interactive test for manual verification with actual audio"""
    print("\nInteractive Test Mode with Audio")
    print("Enter distances to test or 'q' to quit")
    print("You will hear the actual beep for each distance!")
    
    beep = SpeakerBeep()
    
    while True:
        user_input = input("\nEnter distance (cm): ").strip()
        
        if user_input.lower() == 'q':
            break
            
        try:
            distance = float(user_input)
            objects = [MockDistanceReading(distance)]
            
            beep.update_closest(objects)
            
            print(f"Distance: {distance}cm")
            print(f"Beep interval: {beep._curr_duration}s")
            
            if beep._curr_duration:
                print("Playing beep...")
                beep.play_beep()
                
                time.sleep(0.15) 
            else:
                print("No beep (safe distance)")
                
        except ValueError:
            print("Please enter a valid number or 'q' to quit")

def main():
    print("SpeakerBeep Class Test")
    print("Test the current version of speakerbeep")
    print("Beep interval: 0.5s (<10cm), 1.5s (10-30cm), 3.0s (30-50cm), None (>50cm)")
    print("=" * 70)

    if not test_audio_system():
        print("\nAudio system is not working. Please check your speakers and volume.")
        return

    all_passed = True

    try:
        all_passed &= test_basic_functionality()
    except Exception as e:
        print(f"Basic functionality test failed: {e}")
        all_passed = False

    try:
        all_passed &= test_audio_playback()
    except Exception as e:
        print(f"Audio playback test failed: {e}")
        all_passed = False

    try:
        all_passed &= test_backup_simulation()
    except Exception as e:
        print(f"Backup simulation test failed: {e}")
        all_passed = False

    try:
        all_passed &= test_stop_functionality()
    except Exception as e:
        print(f"Stop functionality test failed: {e}")
        all_passed = False

    try:
        all_passed &= test_continuous_beeping()
    except Exception as e:
        print(f"Continuous beeping test failed: {e}")
        all_passed = False

    try:
        all_passed &= test_constant_distance()
    except Exception as e:
        print(f"Constant distance test failed: {e}")
        all_passed = False

    # Test continuous alarm loop
    try:
        all_passed &= test_alarm_loop()
    except Exception as e:
        print(f"Alarm loop test failed: {e}")
        all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("✓ All automated tests passed!")
    else:
        print("✗ Some tests failed!")

    print("\nWould you like to run interactive tests? (y/n)")
    choice = input().strip().lower()

    if choice == 'y':
        interactive_test()

    print("\nTest session completed!")

if __name__ == "__main__":
    main()


def test_alarm_loop():
    """Test if alarm_loop keeps beeping while in alarm range"""
    print("\nTesting alarm loop (continuous beep in alarm range)...")
    beep = SpeakerBeep()
    # Simulate distance always in alarm range (<50cm)
    distances = [25] * 5  # 5 cycles, always 25cm
    idx = 0
    def get_distance():
        nonlocal idx
        if idx < len(distances):
            d = distances[idx]
            idx += 1
            return d
        else:
            return 100  # Out of alarm range, should stop
    beep.alarm_loop(get_distance)
    print("✓ Alarm loop exited after leaving alarm range.")
    return True
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ All automated tests passed!")
    else:
        print("✗ Some tests failed!")
    
    print("\nWould you like to run interactive tests? (y/n)")
    choice = input().strip().lower()
    
    if choice == 'y':
        interactive_test()
    
    print("\nTest session completed!")

if __name__ == "__main__":
    main()